import numpy as np
import numba as nb
import prody as pd
import typing
from pathlib import Path


def aligned_string_to_array(aln: str) -> np.ndarray:
    """
    Aligned sequence to array of indices with gaps as -1

    Parameters
    ----------
    aln

    Returns
    -------
    indices
    """
    aln_array = np.zeros(len(aln), dtype=np.int64)
    i = 0
    for j in range(len(aln)):
        if aln[j] != '-':
            aln_array[j] = i
            i += 1
        else:
            aln_array[j] = -1
    return aln_array


@nb.njit
def get_common_positions(aln_sequence_1: np.ndarray, aln_sequence_2: np.ndarray, gap=-1):
    """
    Return positions where neither alignment has a gap

    Parameters
    ----------
    aln_sequence_1
    aln_sequence_2
    gap

    Returns
    -------
    common_positions_1, common_positions_2
    """
    pos_1 = np.array([aln_sequence_1[i] for i in range(len(aln_sequence_1)) if aln_sequence_1[i] != gap and aln_sequence_2[i] != gap])
    pos_2 = np.array([aln_sequence_2[i] for i in range(len(aln_sequence_2)) if aln_sequence_1[i] != gap and aln_sequence_2[i] != gap])
    return pos_1, pos_2


def get_aligned_coordinates(aln_array: np.ndarray, coords, gap=-1):
    """
    Fills coordinates according to an alignment
    gaps (-1) in the sequence correspond to NaNs in the aligned coordinates

    Parameters
    ----------
    aln_array
        sequence (with gaps)
    coords
        coordinates of atoms corresponding to alignment with NaNs in gap positions
    gap
        character that represents gaps
    Returns
    -------
    aligned coordinates
    """
    pos = [i for i in range(len(aln_array)) if aln_array[i] != gap]
    assert len(pos) == coords.shape[0]
    aln_coords = np.zeros((len(aln_array), 3))
    aln_coords[:] = np.nan
    aln_coords[pos] = coords
    return aln_coords


def get_file_parts(input_filename: typing.Union[str, Path]) -> tuple:
    """
    Gets directory path, name, and extension from a filename
    Parameters
    ----------
    input_filename

    Returns
    -------
    (path, name, extension)
    """
    input_filename = Path(input_filename)
    path = str(input_filename.parent)
    extension = input_filename.suffix
    name = input_filename.stem
    return path, name, extension


def get_alpha_indices(protein):
    """
    Get indices of alpha carbons of pd AtomGroup object
    """
    return [a.getIndex() for a in protein.iterAtoms() if a.getName() == 'CA']


def get_beta_indices(protein: pd.AtomGroup) -> list:
    """
    Get indices of beta carbons of pd AtomGroup object
    (alpha if Gly)
    """
    return [a.getIndex() for a in protein.iterAtoms() if
            (a.getResname() != 'GLY' and a.getName() == 'CB') or (a.getResname() == 'GLY' and a.getName() == 'CA')]
