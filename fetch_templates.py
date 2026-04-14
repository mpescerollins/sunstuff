import numpy as np
import os
from scipy.io import readsav
import h5py
import glob

#simple script to download the narrow line abroad line templates from the web and convert them from .sav 
# to .txt files and to hdf5 to use in threeML

"""
Notes from https://sohoftp.nascom.nasa.gov/solarsoft/packages/spex/idl/object_spex/gamma_ray_templates_help.txt
Pho - an elemental composition similar to that found in the solar photosphere.
Cor - an elemental composition similar to that found in gradual solar energetic particle events or in the corona.
Rea - an elemental composition found in impulsive solar energetic particle events defined by Don Reames (rea).  
(So pho-cor are templates for a photospheric ambient abundance and a gradual or coronal accelerated particle abundance)
"""


def convert_sav_to_txt(sav_file):
    data = readsav(sav_file)
    x = data['enucl']
    y = data['fnucl']
    # Combine into two columns
    out = np.column_stack((x, y))
    np.savetxt("%s.txt"%sav_file.split('.')[0], out, header="enucl fnucl",fmt="%.6e" )
    

def convert_txt_to_hdf5(template_type, line_type):

    all_flux = []
    proton_index = []

    energy_ref = None
    #cwd = os.getcwd()
    #folder_path = os.path.join(cwd, local_folder)
    files = sorted(glob.glob(f"*{line_type}*.txt"))
    print(files)
    print(f"Found {len(files)} files  for template type {line_type}")

    for filepath in files:
        data = np.loadtxt(filepath)
    
        energy = data[:, 0]
        flux = data[:, 1]
    
        # Check energy grid consistency
        if energy_ref is None:
            energy_ref = energy
        else:
            if not np.allclose(energy_ref, energy):
                raise ValueError(f"Energy grid mismatch in {filepath}")
    
        all_flux.append(flux)
    
    #The value of the proton index is in the filename, for example pp_brd_ap022_s160_th00.txt has a proton index of 160, 
    #which corresponds to 1.60, but I first need to remove the 's' and then divide by 100.0    

        name = os.path.basename(filepath)
        value = name.split("_")[3]
        value = float(value.strip('s')) / 100.0
        proton_index.append(value)
    
    # Convert to arrays
    all_flux = np.array(all_flux)   
    proton_index = np.array(proton_index)
    print(f"Energy grid: {energy_ref}")
    print(f"Proton index: {proton_index}")
    print(f"Flux shape: {all_flux.shape}")
    print(f"Proton index shape: {proton_index.shape}")
    # Save to HDF5
    #Save the hdf5 file with the same name as the local folder
    local_folder = os.getcwd()
    _name = local_folder.split('/')[-1]
   
    hdf5_file_name = '{}_{}.h5'.format(line_type, _name)
    print(f"Saving {hdf5_file_name}...")
    
    with h5py.File(hdf5_file_name, "w") as f:
        f.create_dataset("energies", data=energy_ref)
        f.create_dataset("grid", data=all_flux)
        f.create_dataset("parameters/s", data=proton_index)
        dt = h5py.string_dtype(encoding='utf-8')
        f.create_dataset("parameter_order", data=["s"], dtype=dt)

        f.attrs["name"] = hdf5_file_name.split('.')[0]
        f.attrs["description"] = "template for proton-proton interactions"
        f.attrs['interpolation_degree'] = 1
        f.attrs['spline_smoothing_factor'] = 0.0    

    print("Done!")  


def download_and_convert(template_type,ar_angle, ambient_abundance, accelerated_part_abundance, line_type):

    base_url = "https://hesperia.gsfc.nasa.gov/rhessi_extras/gamma_ray_templates/"

    base_url_angle = f"{base_url}{template_type}/{template_type}_{ambient_abundance}_{accelerated_part_abundance}/{template_type}_{ambient_abundance}_{accelerated_part_abundance}_theta{ar_angle:02}/"
    
    proton_indexes = list(range(160, 601, 20))
    #Create a local folder with the same name as the remote folder to save the files
    local_folder = f"{template_type}_{ambient_abundance}_{accelerated_part_abundance}_theta{ar_angle:02}"

    if not os.path.exists(local_folder):
        os.makedirs(local_folder)
    os.chdir(local_folder)

    for index in proton_indexes:
        if accelerated_part_abundance == 'rea':
            template_name = 'pr'
        else:
            template_name = 'pp'
        #Here I am getting by default the templates with alpha to proton ratio of 0.22, but I could also get the ones with 0.1 by changing the ap022 to ap010 in the filename
        filename = f"{template_name}_{line_type}_ap022_s{index}_th{ar_angle:02}.sav"
        url = f"{base_url_angle}{filename}"
        #cd to the local folder
        
        #Check to see if the file already exists, if it does skip the download
        if os.path.exists(filename.split('.')[0]+'.txt'):
            print(f"{filename.split('.')[0]+'.txt'} already exists, skipping download...")
            continue
        print(f"Downloading {url} to {local_folder}...")
        os.system(f"wget {url}")
        convert_sav_to_txt(filename)
        os.remove(filename)
    #Then convert the txt files to hdf5    
    convert_txt_to_hdf5(local_folder, line_type)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ambient_abund', type=str, default='pho', help='Ambient abundance (pho, cor, rea). Default is pho')
    parser.add_argument('--accel_part_abund', type=str, default='rea', help='Accelerated particle abundance (pho, cor, rea). Default is rea')
    parser.add_argument('--ar_angle', type=int, default=30, help='Heliocentric angle of the flare site from Sun center  (e.g., 30, 43, 60, 75, 90). Default is 30')
    parser.add_argument('--template_type', type=str, default='3comp', help='Template type (e.g. abun pions 22scat). Default is 3comp')
    parser.add_argument('--line_type', type=str, default='nar', help='Line type (e.g. nar, brd). Default is nar')
    args = parser.parse_args()
    print(args)
    download_and_convert(args.template_type, args.ar_angle, args.ambient_abund, args.accel_part_abund, args.line_type)

