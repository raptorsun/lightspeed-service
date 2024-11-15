"""Score calculation for evaluation."""

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from rouge_score.rouge_scorer import RougeScorer
from scipy.spatial.distance import cosine, euclidean


class ResponseScore:
    """Calculate response score."""

    def __init__(self, metrics):
        """Initialize."""
        self._embedding_model = HuggingFaceEmbedding(
            "sentence-transformers/all-mpnet-base-v2"
        )
        self._rouge_scorer = RougeScorer(["rougeL"], use_stemmer=True)

        self._relevancy_scorer = None
        if "answer_relevancy" in metrics:
            # Importing here to avoid setting up judge LLM in config, if not required.
            from .relevancy_score import AnswerRelevancyScore

            self._relevancy_scorer = AnswerRelevancyScore(self._embedding_model)

    def calculate_scores(self, query, answer, response):
        """Calculate different similarity scores for two strings."""
        res_vec = self._embedding_model.get_text_embedding(response)
        ans_vec = self._embedding_model.get_text_embedding(answer)

        # Distance score
        cos_score = 1 - cosine(res_vec, ans_vec)
        euc_score = 1 - euclidean(res_vec, ans_vec)

        len_res, len_ans = len(response), len(answer)
        len_score = 1 - (abs(len_res - len_ans) / (len_res + len_ans))

        # text based scores
        rouge_score = self._rouge_scorer.score(target=answer, prediction=response)

        relevancy_score = answer_valid_flag = generated_questions = None
        if self._relevancy_scorer:
            relevancy_score, answer_valid_flag, generated_questions = (
                self._relevancy_scorer.get_score(query, response)
            )

        print(
            f"cos_score: {cos_score}, "
            f"euc_score: {euc_score}, "
            f"len_score: {len_score}, "
            f"rouge_score: {rouge_score}, "
            f"relevancy_score: {relevancy_score}"
        )
        return (
            cos_score,
            euc_score,
            len_score,
            rouge_score["rougeL"].precision,
            rouge_score["rougeL"].recall,
            rouge_score["rougeL"].fmeasure,
            relevancy_score,
            # Return additional information
            answer_valid_flag,
            generated_questions,
        )
