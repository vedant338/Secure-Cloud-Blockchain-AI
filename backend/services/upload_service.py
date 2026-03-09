import logging
from cloud_storage.upload_to_s3 import process_and_upload_file
from ai_ml.ai_service import analyze_file_risk
from security.hash_utils import calculate_entropy

logger = logging.getLogger("upload_service")

def handle_upload(file_bytes: bytes, filename: str):
    logger.info("Starting encryption & upload process")

    result = process_and_upload_file(file_bytes, filename)

    entropy = calculate_entropy(file_bytes)

    ai_result = analyze_file_risk(
        file_size=len(file_bytes),
        entropy=entropy,
        hash_length=len(result["hash"]),
        verified=1
    )

    result["ai_analysis"] = ai_result

    logger.info("Upload workflow completed")
    return result