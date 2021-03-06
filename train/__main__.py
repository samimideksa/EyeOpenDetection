from dataset import EyeStateDataset
from nets import EyeStateNet
from dataset.multi_input import MultiInputEyeStateDataset
from nets.multi_input import MultiInputEyeStateNet
import argparse
import dlib
import json

def get_cmd_args():

    with open("config.json") as f:
        data = json.load(f)
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_dir",default="",type=str)
    parser.add_argument("--left",type=bool)
    parser.add_argument("--epochs",default=10,type=int)
    parser.add_argument("--batch_size",default=32,type=int)
    parser.add_argument("--lr",default=1e-4,type=float)
    parser.add_argument("--steps",default=200,type=int)
    parser.add_argument("--weights",default=None,type=str)
    parser.add_argument("--output",default=None,type=str)
    parser.add_argument("--network",default="si",type=str)
    parser.add_argument('--image_size',default=(data["facial_image_size"]["image_height"], data["facial_image_size"]["image_width"]), nargs='+', type=int)
    args = parser.parse_args()
    return args

def main():
    args = get_cmd_args()
    if args.network=="si":
        dataset = EyeStateDataset(args.dataset_dir,image_shape=(args.image_size[0],args.image_size[1]),left_eye=args.left)
        dataset.load_dataset()
        net = EyeStateNet(dataset,left_eye=args.left,
                epochs=args.epochs,batch_size=args.batch_size,image_size=args.image_size,lr=args.lr,steps_per_epoch=args.steps,
                weights=args.weights,output=args.output)
        net.train()
    elif args.network=="mi":
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        dataset = MultiInputEyeStateDataset(args.dataset_dir,predictor,image_shape=(args.image_size[0],args.image_size[1]))
        net = MultiInputEyeStateNet(dataset,epochs=args.epochs,batch_size=args.batch_size,image_size=args.image_size,lr=args.lr,steps_per_epoch=args.steps,weights=args.weights,output=args.output)
        net.train()	
    else:
        print ("Unable to recognize network input type from ",args.network)

if __name__ == "__main__":
    main()
