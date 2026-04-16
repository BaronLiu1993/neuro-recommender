from functools import lru_cache
from tribev2 import TribeModel

@lru_cache(maxsize=1)
def _get_model() -> TribeModel:
	return TribeModel.from_pretrained(
		"facebook/tribev2",
		cache_folder="./cache",
		config_update={"data.num_workers": 0},
	)

def predict_voxels_from_text(text: str, verbose: bool = False):
	if not text or not text.strip():
		raise ValueError("text must not be empty")

	model = _get_model()
	events = model.get_events_dataframe(text=text)
	preds, segments = model.predict(events=events, verbose=verbose)
	return preds, segments


preds, segments = predict_voxels_from_text("The cat sat on the mat.")
print(preds.shape)  
print(len(segments))