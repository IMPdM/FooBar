from db.queries.Sunstone.EOLAttachmentBody import EOLAttachmentBodyForTrain
from algo.models.threshold_predictor import predict_threshold, THRESHOLD

from utils.time import DateWindow
from utils.plants import Plants

from db.run_query import run_query
from db.connection import get_engine

import pandas as pd

def main():
	engine = get_engine()

	plant = Plants().get_plant("Sunstone_EOL_Att_Body")

	window = DateWindow.today()
	start = window["start_time"]
	end = window["end_time"]

	query = EOLAttachmentBodyForTrain(plant)
	df = run_query(engine, query, params=(start, end))
	print(df[-10:])

	mean_slope = 0.0001007

	# --------------------------------------------------
	# 2) pokliči naš novi algoritem
	# --------------------------------------------------
	prediction = predict_threshold(
		df=df,
		slope_per_sample=mean_slope,
		threshold=THRESHOLD,
	)
	
	
	print("=== Threshold prediction ===")
	# print(f"Mode: {prediction.mode}")
	print(f"Last value: {prediction.last_value}")
	print(f"Line stopped: {prediction.line_stopped}")
	print(f"Samples to threshold (ceil): {prediction.samples_to_threshold_ceil}")
	print(f"Time to threshold: {prediction.time_to_threshold}")
	# print(f"Avg interval: {prediction.avg_interval}")
    
	now = pd.Timestamp.now()

	if prediction.time_to_threshold is not None:
		error_time = now + prediction.time_to_threshold
		print(f"Now: {now}")
		print(f"Predicted error time: {error_time}")
	else:
		print(f"Now: {now}")
		print("Predicted error time: N/A (no time_to_threshold)")

if __name__ == "__main__":
	main()
