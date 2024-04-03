import pandas as pd
from google.cloud import language_v1
from statistics import mean


def analyze_comment(client, text_content):
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    entities = client.analyze_entities(document=document)
    syntax = client.analyze_syntax(document=document)
    return sentiment, entities, syntax


def calculate_averages(analyses):
    sentiment_scores = [sentiment.score for sentiment, _, _ in analyses]
    sentiment_magnitudes = [sentiment.magnitude for sentiment, _, _ in analyses]
    entity_counts = [len(entities.entities) for _, entities, _ in analyses]
    sentence_counts = [len(syntax.sentences) for _, _, syntax in analyses]

    return {
        'average_sentiment_score': mean(sentiment_scores),
        'average_sentiment_magnitude': mean(sentiment_magnitudes),
        'average_entity_count': mean(entity_counts),
        'average_sentence_count': mean(sentence_counts)
    }


def process_csv(client, file_path):
    df = pd.read_csv(file_path)
    gpt_comments = df['gpt_comment']
    human_comments = df['human_comment']

    gpt_analyses = [analyze_comment(client, comment) for comment in gpt_comments]
    human_analyses = [analyze_comment(client, comment) for comment in human_comments]

    return calculate_averages(gpt_analyses), calculate_averages(human_analyses)


def main():
    client = language_v1.LanguageServiceClient()
    techniques = ['zeroShot', 'fewShot', 'chainOfThought']
    file_paths = ['./PromptingCommentEvaluation/zeroShot.csv', './PromptingCommentEvaluation/fewShot.csv', './PromptingCommentEvaluation/chainOfThought.csv']

    for technique, file_path in zip(techniques, file_paths):
        gpt_results, human_results = process_csv(client, file_path)

        print(f"\n{technique} Technique Evaluation:")
        print(f"GPT Comments: {gpt_results}")
        print(f"Human Grader Comments: {human_results}")


if __name__ == "__main__":
    main()
