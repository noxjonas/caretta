from pathlib import Path

import numpy as np
import prody as pd

from caretta import helper


# TODO: Use multiprocessing to parallelize extraction of features for many proteins:
#     with multiprocessing.Pool(processes=num_main_threads) as pool:
#         pool.starmap(get_dssp_features,
#                      [(protein, pdb_file, dssp_dir)
#                       for (protein, pdb_file) in list_of_proteins])
#     use just pool.map for the others since it's single input


def get_anm_fluctuations(protein: pd.AtomGroup, n_modes: int = 50):
    """
    Get atom fluctuations using an Anisotropic network model with n_modes modes.
    """
    protein_anm, _ = pd.calcANM(protein, n_modes=n_modes, selstr='all')
    return pd.calcSqFlucts(protein_anm)


def get_gnm_fluctuations(protein: pd.AtomGroup, n_modes: int = 50):
    """
    Get atom fluctuations using a Gaussian network model with n_modes modes.
    """
    protein_gnm, _ = pd.calcGNM(protein, n_modes=n_modes, selstr='all')
    return pd.calcSqFlucts(protein_gnm)


def get_dssp_features(protein: pd.AtomGroup, pdb_file: str, dssp_dir: str):
    """
    Gets dssp features

    Parameters
    ----------
    protein
    pdb_file
    dssp_dir

    Returns
    -------
    dict of dssp_
    NH_O_1_index, NH_O_1_energy
        hydrogen bonds; e.g. -3,-1.4 means: if this residue is residue i then N-H of I is h-bonded to C=O of I-3 with an
        electrostatic H-bond energy of -1.4 kcal/mol. There are two columns for each type of H-bond, to allow for bifurcated H-bonds.
    NH_O_2_index, NH_O_2_energy
    O_NH_1_index, O_NH_1_energy
    O_NH_2_index, O_NH_2_energy
    acc
        number of water molecules in contact with this residue *10. or residue water exposed surface in Angstrom^2.
    alpha
        virtual torsion angle (dihedral angle) defined by the four Cα atoms of residues I-1,I,I+1,I+2.Used to define chirality.
    kappa
        virtual bond angle (bend angle) defined by the three Cα atoms of residues I-2,I,I+2. Used to define bend (structure code ‘S’).
    phi
        IUPAC peptide backbone torsion angles.
    psi
        IUPAC peptide backbone torsion angles.
    tco
        cosine of angle between C=O of residue I and C=O of residue I-1. For α-helices, TCO is near +1, for β-sheets TCO is near -1.

    Ignores:
    dssp_bp1, dssp_bp2, and dssp_sheet_label: residue number of first and second bridge partner followed by one letter sheet label
    """
    pdb_file = Path(pdb_file)
    if not pdb_file.exists():
        pd.writePDB(str(pdb_file), protein)
    _, name, _ = helper.get_file_parts(pdb_file)
    dssp_file = pd.execDSSP(str(pdb_file), outputname=name, outputdir=str(dssp_dir))
    protein = pd.parseDSSP(dssp=dssp_file, ag=protein, parseall=True)
    dssp_ignore = ["dssp_bp1", "dssp_bp2", "dssp_sheet_label", "dssp_resnum"]
    dssp_labels = [label for label in protein.getDataLabels() if label.startswith("dssp") and label not in dssp_ignore]
    data = {}
    alpha_indices = helper.get_alpha_indices(protein)
    indices = [protein[x].getData("dssp_resnum") for x in alpha_indices]
    for label in dssp_labels:
        label_to_index = {i - 1: protein[x].getData(label) for i, x in zip(indices, alpha_indices)}
        data[f"{label}"] = np.array([label_to_index[i] if i in label_to_index else 0 for i in range(len(alpha_indices))])
    return data