import json
import logging
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnswerType(Enum):
    """答案类型枚举"""
    MULTIPLE_CHOICE = "multiple_choice"  # A, B, C, D
    BOOLEAN = "boolean"  # 是/否, 对/错, YES/NO
    STRUCTURED = "structured"  # 结构化答案


@dataclass
class AnswerPattern:
    """答案匹配模式配置"""
    pattern: str
    answer_type: AnswerType
    priority: int = 1
    case_sensitive: bool = False
    
    def __post_init__(self):
        """编译正则表达式以提高性能"""
        flags = 0 if self.case_sensitive else re.IGNORECASE
        self.compiled_pattern = re.compile(self.pattern, flags)


class AnswerConfig:
    """答案提取配置类"""
    
    # 预编译的答案模式
    ANSWER_PATTERNS = [
        # 高优先级：明确的答案标识
        AnswerPattern(
            r'答案[：:]\s*([ABCD\s]+|是|否|对|错|正确|错误|YES|NO)(?:\s*\n|$)',
            AnswerType.MULTIPLE_CHOICE,
            priority=1
        ),
        AnswerPattern(
            r'answer[：:]\s*([ABCD\s]+|是|否|对|错|正确|错误|YES|NO)(?:\s*\n|$)',
            AnswerType.MULTIPLE_CHOICE,
            priority=1
        ),
        
        # 中优先级：格式化回答
        AnswerPattern(
            r'是否涉及漏洞[：:]\s*(是|否)',
            AnswerType.BOOLEAN,
            priority=2
        ),
        AnswerPattern(
            r'是否[^：:]*[：:]\s*(是|否)',
            AnswerType.BOOLEAN,
            priority=2
        ),
    ]
    
    # 结构化答案关键词
    STRUCTURED_KEYWORDS = [
        ['影响的组件：', '版本号：'],
        ['是否涉及漏洞：', '漏洞号：'],
        ['是否涉及漏洞：', '影响的产品及版本：'],
        ['Influenced package and version:']
    ]
    
    # 有效答案映射
    VALID_ANSWERS = {
        # 选择题答案
        'multiple_choice': {
            r'^[ABCD]+$': lambda x: x,
            r'^[ABCD](\s+[ABCD])*$': lambda x: re.sub(r'\s+', '', x),
        },
        # 布尔型答案
        'boolean': {
            r'^正\s*确$': '正确',
            r'^错\s*误$': '错误',
            r'^YES$': 'YES',
            r'^NO$': 'NO',
            r'^(是|否|对|错|正确|错误)$': lambda x: x
        }
    }


class AnswerExtractor(ABC):
    """答案提取器抽象基类"""
    
    @abstractmethod
    def can_extract(self, text: str) -> bool:
        """判断是否能处理该文本"""
        pass
    
    @abstractmethod
    def extract(self, text: str) -> str:
        """提取答案"""
        pass


class StructuredAnswerExtractor(AnswerExtractor):
    """结构化答案提取器"""
    
    def can_extract(self, text: str) -> bool:
        """检查是否包含结构化答案关键词"""
        for keywords in AnswerConfig.STRUCTURED_KEYWORDS:
            if len(keywords) == 1:
                if keywords[0] in text:
                    return True
            else:
                if all(keyword in text for keyword in keywords):
                    return True
        return False
    
    def extract(self, text: str) -> str:
        """提取结构化答案"""
        if self.can_extract(text):
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            return '\n'.join(lines)
        return ""


class PatternAnswerExtractor(AnswerExtractor):
    """基于模式的答案提取器"""
    
    def __init__(self, patterns: List[AnswerPattern]):
        self.patterns = sorted(patterns, key=lambda x: x.priority)
    
    def can_extract(self, text: str) -> bool:
        """检查是否有匹配的模式"""
        return any(pattern.compiled_pattern.search(text) for pattern in self.patterns)
    
    def extract(self, text: str) -> str:
        """使用模式提取答案"""
        for pattern in self.patterns:
            match = pattern.compiled_pattern.search(text)
            if match:
                raw_answer = match.group(1).strip()
                return self._normalize_answer(raw_answer)
        return ""
    
    def _normalize_answer(self, answer: str) -> str:
        """规范化答案"""
        if not answer:
            return ""
        
        answer = answer.strip()
        
        # 检查多选题答案
        for pattern, handler in AnswerConfig.VALID_ANSWERS['multiple_choice'].items():
            if re.match(pattern, answer):
                return handler(answer) if callable(handler) else handler
        
        # 检查布尔型答案
        for pattern, handler in AnswerConfig.VALID_ANSWERS['boolean'].items():
            if re.match(pattern, answer, re.IGNORECASE):
                return handler(answer) if callable(handler) else handler
        
        return ""


class DirectAnswerExtractor(AnswerExtractor):
    """直接答案提取器（整个文本就是答案）"""
    
    def can_extract(self, text: str) -> bool:
        """检查整个文本是否是有效答案"""
        normalized = self._normalize_answer(text.strip())
        return bool(normalized)
    
    def extract(self, text: str) -> str:
        """直接返回规范化的文本"""
        return self._normalize_answer(text.strip())
    
    def _normalize_answer(self, answer: str) -> str:
        """规范化答案（复用PatternAnswerExtractor的逻辑）"""
        extractor = PatternAnswerExtractor([])
        return extractor._normalize_answer(answer)


class AnswerExtractionChain:
    """答案提取责任链"""
    
    def __init__(self):
        self.extractors = [
            StructuredAnswerExtractor(),
            PatternAnswerExtractor(AnswerConfig.ANSWER_PATTERNS),
            DirectAnswerExtractor()
        ]
    
    def extract_answer(self, prediction_text: str) -> str:
        """
        从预测文本中智能提取答案
        
        Args:
            prediction_text: 预测文本
            
        Returns:
            提取的答案，如果无法提取则返回空字符串
        """
        if not prediction_text:
            return ""
        
        text = prediction_text.strip()
        
        for extractor in self.extractors:
            try:
                if extractor.can_extract(text):
                    result = extractor.extract(text)
                    if result:
                        logger.debug(f"使用 {extractor.__class__.__name__} 提取到答案: {result}")
                        return result
            except Exception as e:
                logger.warning(f"提取器 {extractor.__class__.__name__} 处理失败: {e}")
                continue
        
        logger.debug(f"无法从文本中提取答案: {text[:100]}...")
        return ""


class PredictionProcessor:
    """预测结果处理器"""
    
    def __init__(self, extraction_chain: Optional[AnswerExtractionChain] = None):
        self.extraction_chain = extraction_chain or AnswerExtractionChain()
    
    def process_predictions(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path]
    ) -> bool:
        """
        处理预测结果文件
        
        Args:
            input_path: 输入JSON文件路径
            output_path: 输出JSON文件路径
            
        Returns:
            处理是否成功
        """
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        # 验证输入文件
        if not self._validate_input_file(input_path):
            return False
        
        try:
            # 读取数据
            data = self._load_json_data(input_path)
            if data is None:
                return False
            
            # 处理数据
            output_data = self._process_data(data)
            
            # 保存结果
            return self._save_results(output_data, output_path)
            
        except Exception as e:
            logger.error(f"处理过程中发生错误: {e}")
            return False
    
    def _validate_input_file(self, input_path: Path) -> bool:
        """验证输入文件"""
        if not input_path.exists():
            logger.error(f"输入文件不存在: {input_path}")
            return False
        
        if not input_path.is_file():
            logger.error(f"输入路径不是文件: {input_path}")
            return False
        
        if input_path.suffix.lower() != '.json':
            logger.warning(f"输入文件不是JSON格式: {input_path}")
        
        return True
    
    def _load_json_data(self, input_path: Path) -> Optional[Dict[str, Any]]:
        """加载JSON数据"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"成功加载数据文件: {input_path}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"JSON格式错误: {e}")
            return None
        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            return None
    
    def _process_data(self, data: Dict[str, Any]) -> List[Dict[str, Union[int, str]]]:
        """处理数据"""
        output_data = []
        question_id = 1
        
        # 确保键按数字顺序排序
        try:
            sorted_keys = sorted(data.keys(), key=lambda x: int(x))
        except ValueError:
            logger.warning("键不是数字格式，使用字符串排序")
            sorted_keys = sorted(data.keys())
        
        processed_count = 0
        skipped_count = 0
        
        for key in sorted_keys:
            entry = data[key]
            
            if not isinstance(entry, dict):
                logger.warning(f"键 '{key}' 对应的值不是字典，已跳过")
                skipped_count += 1
                continue
            
            if "prediction" not in entry:
                logger.warning(f"键 '{key}' 缺少 'prediction' 字段，已跳过")
                skipped_count += 1
                continue
            
            prediction_content = entry["prediction"]
            extracted_answer = self.extraction_chain.extract_answer(prediction_content)
            
            output_data.append({
                "question_id": question_id,
                "answer": extracted_answer
            })
            
            question_id += 1
            processed_count += 1
        
        logger.info(f"处理完成: 成功处理 {processed_count} 条，跳过 {skipped_count} 条")
        return output_data
    
    def _save_results(
        self, 
        output_data: List[Dict[str, Union[int, str]]], 
        output_path: Path
    ) -> bool:
        """保存结果"""
        try:
            # 确保输出目录存在
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"成功生成文件: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存文件失败: {e}")
            return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='处理预测结果文件')
    parser.add_argument('input_file', help='输入JSON文件路径')
    parser.add_argument('output_file', help='输出JSON文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细日志输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    processor = PredictionProcessor()
    success = processor.process_predictions(args.input_file, args.output_file)
    
    if not success:
        exit(1)


if __name__ == "__main__":
    # 可以直接运行或通过命令行参数运行
    if len(os.sys.argv) == 1:
        # 默认路径（用于向后兼容）
        input_file = "your_input_file.json"
        output_file = "your_output_file.json"
        
        processor = PredictionProcessor()
        processor.process_predictions(input_file, output_file)
    else:
        main() 