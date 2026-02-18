from Tractography import tensorODFStreamlineGeneration
import pickle
import os.path
from fury import window, actor


def run_tractography():
    # filepaths go paths here
    data_fpath = os.path.join(os.path.dirname(__file__), "input_data", "sub-1000__dwi.nii.gz")
    bval_fpath = os.path.join(os.path.dirname(__file__), "input_data", "sub-1000__dwi.bval")
    bvec_fpath = os.path.join(os.path.dirname(__file__), "input_data", "sub-1000__dwi.bvec")
    mask_fpath = os.path.join(os.path.dirname(__file__), "input_data", "sub-1000__mask_wm.nii.gz")

    # run the tractography. may take a while
    streamlines = tensorODFStreamlineGeneration(
        data_fpath,
        bvec_fpath,
        bval_fpath,
        mask_fpath,
        rel_peak_threshold=0.99,
        min_separation_angle=180,
        max_len=500,
        seed_density=[1, 1, 1],
        return_all=True
    )

    # output filepaths go here, save the output (saves the nibabel.array_sequence object returned by tractography)
    output_fpath = os.path.join(os.path.dirname(__file__), "output_data", "output_streamlines.pkl")
    with open(output_fpath, "wb") as outp:
        pickle.dump(streamlines, outp)


def view_tractography():
    streamlines_fpath = os.path.join(os.path.dirname(__file__), "output_data", "output_streamlines.pkl")
    with open(streamlines_fpath, "rb") as inp:
        streamlines = pickle.load(inp)

    scene = window.Scene()
    scene.add(actor.streamtube(streamlines))
    window.show(scene)


if __name__ == "__main__":
    # run_tractography()
    view_tractography()
