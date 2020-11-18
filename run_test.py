import argparse
import os

parser = argparse.ArgumentParser(description='Generate Test Results While Training')
parser.add_argument("--models_dir", type=str, required=True, help="")
parser.add_argument("--log_dir", type=str, required=True, help="")
parser.add_argument("--base_step", type=int, default=0)
parser.add_argument("--input_dir", type=str, required=True)
parser.add_argument("--which_direction", type=str, default="AtoB")
parser.add_argument("--max_step", type=int, default=-1)
args = parser.parse_args()
steps = set()
while True:
	files = os.listdir(args.models_dir)
	files = [int(i[6:-5]) for i in files if i[-5:] == ".meta"]
	files = sorted([i for i in files if i not in steps])
	for s in files:
		if s < args.base_step: continue
		if args.max_step != -1 and s > args.max_step: continue
		steps.add(s)
		print("Step", s)

		os.system("python pix2pix.py --mode test --output_dir %s --input_dir %s --checkpoint %s --load_step %d --which_direction %s" % (os.path.join(args.log_dir, str(s)), args.input_dir, args.models_dir, s, args.which_direction))
		imgs = os.path.join(args.log_dir, str(s), "images")
		ims = os.listdir(imgs)
		for f in ims:
			if "outputs" not in f: os.system("rm %s" % (os.path.join(imgs,f),))

