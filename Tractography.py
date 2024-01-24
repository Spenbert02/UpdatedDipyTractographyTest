import dipy.reconst.dti as dti
from dipy.core.gradients import gradient_table
from dipy.data import get_sphere
from dipy.direction import peaks_from_model
from dipy.io import read_bvals_bvecs
from dipy.tracking.stopping_criterion import BinaryStoppingCriterion
from dipy.tracking.local_tracking import LocalTracking
from dipy.tracking.streamline import Streamlines
from dipy.tracking import utils
from dipy.io.image import load_nifti


def tensorODFStreamlineGeneration(scan_data_fpath, bvec_fpath, bval_fpath, mask_fpath, rel_peak_threshold=0.99, min_separation_angle=180,
                                  max_len=500, seeds=None, seed_density=[2, 2, 2], return_all=True):
    """
    run streamline tracking using dipy and the tensor odf, and return the resultant streamline set. can take a while to run.
    - scan_data_fpath: file path to the scan data.
    - bvec_fpath: file path to the bvecs
    - bval_fpath: file path to the bvals
    - mask_fpath: file path to the mask to use for tractography
    - rel_peak_treshold: the relative peak threshold to use for tractography. only peaks in the model that are above this percentage
      of the maximum peak height will be returned
    - min_separation_angle: peaks must be separated by at least this angle in order to be considered. set to 180, only one peak will
      be generated for each odf
    - max_len: maximum length of fibers to track (in mm)
    - seeds: optional, n by 3 array of points to seed tractography. volume seeding is used if this is None
    - seed_density: 1 by 3 array, [2, 2, 2] by default, density of seeds if no predetermined seeds given
    - return_all: bool, return_all parameter in LocalTracking creation
    """
                                    
    scan_data, scan_affine = load_nifti(scan_data_fpath)  # import heart
    bvals, bvecs = read_bvals_bvecs(bval_fpath, bvec_fpath)  # load bvals and bvecs
    mask_data, mask_affine = load_nifti(mask_fpath)  # import mask
    
    # creating tensor model
    gtab = gradient_table(bvals, bvecs)
    tenmodel = dti.TensorModel(gtab)

    # discretized sphere for odfs
    sphere = get_sphere("symmetric362")

    # getting peaks and metrics
    tensor_peaks = peaks_from_model(tenmodel, 
                                    scan_data, 
                                    sphere, 
                                    relative_peak_threshold=rel_peak_threshold,  # we want only the primary direction no matter what
                                    min_separation_angle=min_separation_angle,  # should mean only one direction is used, no matter what 
                                    mask=(mask_data == 1))

    # mask for seeding and stopping criterion
    bool_mask = mask_data
    stopping_criterion = BinaryStoppingCriterion(bool_mask)
    if seeds is None:
        seeds = utils.seeds_from_mask(bool_mask, scan_affine, seed_density)

    # Set up and compute streamlines
    STEP_LENGTH = 0.5
    streamlines_generator = LocalTracking(direction_getter=tensor_peaks,
                                          stopping_criterion=stopping_criterion,
                                          seeds=seeds,
                                          affine=scan_affine,
                                          step_size=STEP_LENGTH,
                                          max_cross=1,
                                          maxlen=int(max_len / STEP_LENGTH),
                                          fixedstep=True,
                                          return_all=return_all)
    streamlines = Streamlines(streamlines_generator)
    
    return streamlines