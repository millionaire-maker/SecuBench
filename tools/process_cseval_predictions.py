"""
CS-Eval预测结果处理工具

用于提取OpenCompass评测结果中的模型预测内容，并转换为CS-Eval官网提交格式。

使用方法：
    python process_cseval_predictions.py --input <输入文件路径> --output <输出文件路径>

示例：
    python process_cseval_predictions.py \
        --input results/SecGPT-7B/predictions/cs-eval-questions.jsonl \
        --output results/SecGPT-7B/cs_eval_submission.json
"""

import json
import os
import argparse


def process_predictions(input_json_path, output_json_path):
    """
    提取指定JSON文件中 'prediction' 的内容，并生成一个新的JSON文件。

    Args:
        input_json_path (str): 输入JSON文件的路径。
        output_json_path (str): 输出JSON文件的路径。
    """
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 '{input_json_path}'。")
        return False
    except json.JSONDecodeError:
        print(f"❌ 错误：无法解析文件 '{input_json_path}' 为有效的 JSON 格式。")
        return False

    output_data = []
    question_id = 1

    # 假设输入JSON的键是字符串形式的数字，需要按顺序处理
    # 将键转换为整数并排序，以确保question_id的顺序正确
    try:
        sorted_keys = sorted(data.keys(), key=lambda x: int(x))
    except ValueError:
        print(f"❌ 错误：JSON文件中的键不是数字格式，无法排序。")
        return False

    for key in sorted_keys:
        entry = data[key]
        if "prediction" in entry:
            prediction_content = entry["prediction"]
            output_data.append({
                "question_id": question_id,
                "answer": prediction_content
            })
            question_id += 1
        else:
            print(f"⚠️  警告：键 '{key}' 下的条目没有 'prediction' 字段，已跳过。")

    if not output_data:
        print(f"❌ 错误：没有找到任何有效的预测结果。")
        return False

    # 确保输出目录存在
    output_dir = os.path.dirname(output_json_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 创建输出目录：{output_dir}")

    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"✅ 成功生成文件：'{output_json_path}'")
        print(f"📊 处理了 {len(output_data)} 个预测结果")
        return True
    except IOError as e:
        print(f"❌ 错误：写入文件 '{output_json_path}' 时发生错误：{e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="CS-Eval预测结果处理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  python process_cseval_predictions.py \
      --input results/SecGPT-7B/predictions/cs-eval-questions.jsonl \
      --output results/SecGPT-7B/cs_eval_submission.json

处理完成后，请前往 CS-Eval 官网提交生成的JSON文件：
  https://cs-eval.com/#/app/submission
        """.strip()
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='输入的预测结果JSON文件路径'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='输出的CS-Eval提交格式JSON文件路径'
    )
    
    args = parser.parse_args()
    
    print("🚀 开始处理CS-Eval预测结果...")
    print(f"📥 输入文件：{args.input}")
    print(f"📤 输出文件：{args.output}")
    print("-" * 50)
    
    success = process_predictions(args.input, args.output)
    
    if success:
        print("-" * 50)
        print("🎉 处理完成！")
        print("📝 下一步：前往 CS-Eval 官网提交结果文件")
        print("🔗 提交地址：https://cs-eval.com/#/app/submission")
    else:
        print("-" * 50)
        print("💥 处理失败，请检查输入文件格式")
        exit(1)


if __name__ == "__main__":
    main()