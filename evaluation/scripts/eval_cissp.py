"""
CISSP数据集评测脚本
本脚本使用SecGPT-7B模型进行推理，并使用SecGPT-14B模型进行评测，并保存评测结果至outputs/SecGPT_7B文件夹中

使用方法：
1. 指定推理模型和评测模型
2. 运行本脚本
3. 查看outputs/SecGPT_7B文件夹中的评测结果

"""
from mmengine.config import read_base
from opencompass.models.openai_api import OpenAISDK

# Import pre-configured models from OpenCompass
with read_base():
    from opencompass.configs.models.clouditera.SecGPT_7B import (
        models as SecGPT_7B_model,
    )
    from opencompass.configs.models.clouditera.SecGPT_14B import (
        models as SecGPT_14B_model,
    )
from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.evaluator import GenericLLMEvaluator
from opencompass.datasets import generic_llmjudge_postprocess
from opencompass.datasets import CustomDataset


# Dataset reader configuration
math_reader_cfg = dict(input_columns=['question', 'A', 'B', 'C', 'D'], output_column='answer')

# Inference configuration
math_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template=dict(
            round=[
                dict(
                    role='HUMAN',
                    prompt='{question}\nA. {A}\nB. {B}\nC. {C}\nD. {D}\n请你只回答正确答案选项，不要额外的文字描述。',
                ),
            ]
        ),
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=GenInferencer),
)


# Template for the LLM judge
GRADER_TEMPLATE = """
    Please as a grading expert, judge whether the final answers given by the candidates below are consistent with the standard answers, that is, whether the candidates answered correctly. 
    
    Here are some evaluation criteria:
    1. Please refer to the given standard answer. You don't need to re-generate the answer to the question because the standard answer has been given. You only need to judge whether the candidate's answer is consistent with the standard answer according to the form of the question. Don't try to answer the original question. You can assume that the standard answer is definitely correct.
    2. Because the candidate's answer may be different from the standard answer in the form of expression, before making a judgment, please understand the question and the standard answer first, and then judge whether the candidate's answer is correct, but be careful not to try to answer the original question.
    3. Some answers may contain multiple items, such as multiple-choice questions, multiple-select questions, fill-in-the-blank questions, etc. As long as the answer is the same as the standard answer, it is enough. For multiple-select questions and multiple-blank fill-in-the-blank questions, the candidate needs to answer all the corresponding options or blanks correctly to be considered correct.
    4. Some answers may be expressed in different ways, such as some answers may be a mathematical expression, some answers may be a textual description, as long as the meaning expressed is the same. And some formulas are expressed in different ways, but they are equivalent and correct.
    5. If the prediction is given with \\boxed{}, please ignore the \\boxed{} and only judge whether the candidate's answer is consistent with the standard answer.

    Please judge whether the following answers are consistent with the standard answer based on the above criteria. Grade the predicted answer of this new question as one of:
    A: CORRECT 
    B: INCORRECT
    Just return the letters "A" or "B", with no text around it.

    Here is your task. Simply reply with either CORRECT, INCORRECT. Don't apologize or correct yourself if there was a mistake; we are just trying to grade the answer.


    <Original Question Begin>: \n{question}\n<Original Question End>\n\n
    <Gold Target Begin>: \n{answer}\n<Gold Target End>\n\n
    <Predicted Answer Begin>: \n{prediction}\n<Predicted End>\n\n
    
    Judging the correctness of candidates' answers:
""".strip()

# Evaluation configuration using LLM as judge
math_eval_cfg = dict(
    evaluator=dict(
        type=GenericLLMEvaluator,
        prompt_template=dict(
            type=PromptTemplate,
            template=dict(
                begin=[
                    dict(
                        role='SYSTEM',
                        fallback_role='HUMAN',
                        prompt="You are a helpful assistant who evaluates the correctness and quality of models' outputs.",
                    )
                ],
                round=[
                    dict(role='HUMAN', prompt=GRADER_TEMPLATE),
                ],
            ),
        ),
        dataset_cfg=dict(
            type=CustomDataset,
            path='/root/opencompass/data/cissp',
            file_name='cissp.jsonl',
            reader_cfg=math_reader_cfg,
        ),
        judge_cfg=SecGPT_14B_model[0],
        dict_postprocessor=dict(type=generic_llmjudge_postprocess),
    ),
)

# Dataset configuration
datasets = [
    dict(
        type=CustomDataset,
        path='/root/opencompass/data/cissp',
        file_name='cissp.jsonl',
        reader_cfg=math_reader_cfg,
        infer_cfg=math_infer_cfg,
        eval_cfg=math_eval_cfg,
    )
]

# Model to be evaluated
models = SecGPT_7B_model

# Limiting test to first 8 examples for quick testing
# math_reader_cfg['test_range'] = '[0:8]'

# Output directory
work_dir = 'results/SecGPT-7B'
