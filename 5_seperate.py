import os
import json
import random
import utils.make_coco as make_coco

def create_coco():
	return {
		"info": make_coco.add_info(),
		"licenses": make_coco.add_licenses(),
		"categories": make_coco.add_categories(),
		"images": [],
		"annotations": [],
	}

def save_coco(coco_path, coco):
	with open(coco_path, 'w') as outfile:
		json.dump(coco, outfile)

def load_coco(coco_path):
	f = open(coco_path)
	return json.load(f)

# image id -> [anns of that image id]
def maps_annotations(coco):
	anns = {}
	for ann in coco['annotations']:
		if ann['image_id'] in anns:
			anns[ann['image_id']] += [ann]
		else:
			anns[ann['image_id']] = [ann]
	return anns

if __name__ == "__main__":

	# set path
	root = os.path.dirname(os.path.realpath(__file__))

	# load coco
	coco_path = os.path.join(root, "data/output_export/coco.json")
	# coco_path = os.path.join(root, "data/output_export/S1/Plate_07/Testing_set/coco.json")
	coco = load_coco(coco_path)
	print("[ Finish Loading ]")

	# map coco to dictionary
	anns = maps_annotations(coco)
	print("[ Finish Mapping ]")

	# create coco
	train = create_coco()
	test = create_coco()

	# shuffle
	total = len(coco["images"])
	indices = list(range(total))
	train_ratio = 0.8
	train_indices = random.sample(indices, int(total * train_ratio))
	test_indices = [i for i in indices if i not in train_indices]

	count_train = 0
	count_test = 0

	for index in train_indices:
		image = coco['images'][index]
		for ann in anns[image["id"]]:
			if ann['area'] < 10: continue
			count_train += 1
			train['annotations'].append(ann)
			# train['annotations'][-1]['category_id'] = 1
		train['images'].append(image)

	for index in test_indices:
		image = coco['images'][index]
		for ann in anns[image["id"]]:
			if ann['area'] < 10: continue
			count_test += 1
			test['annotations'].append(ann)
			# test['annotations'][-1]['category_id'] = 1
		test['images'].append(image)

	print('training ', count_train)
	print('testing  ', count_test)

	save_coco(os.path.join(root, "train.json"), train)
	save_coco(os.path.join(root, "test.json"), test)