import arcpy
import os

#####################################################################################
# USER INPUTS
#####################################################################################

# Set the working directory to the folder which contains the AOIS subfolder
    # AOIS folder = folder named 'AOIS' that contains the GADM shapefiles
working_directory = r"C:\GIS\carbon_model\CarbonFlux_QA_2023"

# Whether you want to overwrite previous QA outputs
overwrite_output = True

# With each model update, change loss years and model_run_date
    # loss_years = number of years of tree cover loss (if input loss raster is changed, this must be changed, too)
    # model_run_date = s3 directory where per-pixel outputs from most recent model run are saved
loss_years = 22
model_run_date = '20231114'

# List of tile_ids to process (change according to which tiles overlap with your AOIS shapefiles)
tile_list = ['20N_020W', '00N_110E']

#####################################################################################

# Directories to be created/ checked
arcpy.env.workspace = working_directory
aois_folder = os.path.join(arcpy.env.workspace,"AOIS")
input_folder = os.path.join(arcpy.env.workspace,"Input")
mask_folder = os.path.join(arcpy.env.workspace,"Mask")
mask_input_folder = os.path.join(arcpy.env.workspace,"Mask", "Inputs")
mask_output_folder = os.path.join(arcpy.env.workspace,"Mask", "Mask")
gain_folder = os.path.join(mask_input_folder, "Gain")
mangrove_folder = os.path.join(mask_input_folder, "Mangrove")
plantations_folder = os.path.join(mask_input_folder, "Pre_2000_Plantations")
tcd_folder = os.path.join(mask_input_folder, "TCD")
whrc_folder = os.path.join(mask_input_folder, "WHRC")
outputs_folder = os.path.join(arcpy.env.workspace, "Outputs")
csv_folder = os.path.join(outputs_folder, "CSV")
annual_folder = os.path.join(outputs_folder, "Annual")
tcl_folder = os.path.join(arcpy.env.workspace, "TCL")

# Filepaths for tile download step
s3_base_dir = 's3://gfw2-data/climate/carbon_model/'

## Input folder tiles
# Gross emissions per pixel in forest extent
gross_emis_forest_extent_s3_path = os.path.join(s3_base_dir, f'gross_emissions/all_drivers/all_gases/biomass_soil/standard/forest_extent/per_pixel/{model_run_date}/')
gross_emis_forest_extent_s3_pattern = f'gross_emis_all_gases_all_drivers_Mg_CO2e_pixel_biomass_soil_forest_extent_2001_{loss_years}'

# Gross emissions per pixel in all pixels
gross_emis_full_extent_s3_path = os.path.join(s3_base_dir, f'gross_emissions/all_drivers/all_gases/biomass_soil/standard/full_extent/per_pixel/{model_run_date}/')
gross_emis_full_extent_s3_pattern = f'gross_emis_all_gases_all_drivers_Mg_CO2e_pixel_biomass_soil_full_extent_2001_{loss_years}'

# Gross removals per pixel in forest extent
gross_removals_forest_extent_s3_path = os.path.join(s3_base_dir, f'gross_removals_AGCO2_BGCO2_all_forest_types/standard/forest_extent/per_pixel/{model_run_date}/')
gross_removals_forest_extent_s3_pattern = f'gross_removals_AGCO2_BGCO2_Mg_pixel_all_forest_types_forest_extent_2001_{loss_years}'

# Gross removals per pixel in all pixels
gross_removals_full_extent_s3_path = os.path.join(s3_base_dir, f'gross_removals_AGCO2_BGCO2_all_forest_types/standard/full_extent/per_pixel/{model_run_date}/')
gross_removals_full_extent_s3_pattern = f'gross_removals_AGCO2_BGCO2_Mg_pixel_all_forest_types_full_extent_2001_{loss_years}'

# Net flux per pixel in forest extent
netflux_forest_extent_s3_path = os.path.join(s3_base_dir, f'net_flux_all_forest_types_all_drivers/biomass_soil/standard/forest_extent/per_pixel/{model_run_date}/')
netflux_forest_extent_s3_pattern = f'net_flux_Mg_CO2e_pixel_biomass_soil_forest_extent_2001_{loss_years}'

# Net flux per pixel in all pixels
netflux_full_extent_s3_path = os.path.join(s3_base_dir, f'net_flux_all_forest_types_all_drivers/biomass_soil/standard/full_extent/per_pixel/{model_run_date}/')
netflux_full_extent_s3_pattern = f'net_flux_Mg_CO2e_pixel_biomass_soil_full_extent_2001_{loss_years}'

## Mask, Inputs folder tiles
# Hansen removals tiles based on canopy height (2000-2020)
gain_s3_path = 's3://gfw-data-lake/umd_tree_cover_gain_from_height/v202206/raster/epsg-4326/10/40000/gain/geotiff/'
gain_s3_pattern = ''
gain_local_pattern = 'tree_cover_gain_2000_2020'
#TODO: CHECK THIS PATTERN ACROSS THE CODE?

# Processed mangrove aboveground biomass in the year 2000
mangrove_s3_path = os.path.join(s3_base_dir, 'mangrove_biomass/processed/standard/20190220/')
mangrove_s3_pattern = 'mangrove_agb_t_ha_2000'
#TODO: ERIN'S FILES HAVE "_REWINDOW". DOES THIS MATTER -> DO WE NEED TO ADD A REWINDOWING STEP?

# Pre-2000 plantations
plantation_s3_path = os.path.join(s3_base_dir, 'other_emissions_inputs/IDN_MYS_plantation_pre_2000/processed/20200724/')
plantation_s3_pattern = 'plantation_2000_or_earlier_processed'

# Tree cover density 2000 tiles
tcd_s3_path = 's3://gfw2-data/forest_cover/2000_treecover/'
tcd_s3_pattern = 'Hansen_GFC2014_treecover2000'

# Woods Hole aboveground biomass 2000 version 4 tiles
whrc_s3_path = 's3://gfw2-data/climate/WHRC_biomass/WHRC_V4/Processed/'
whrc_s3_pattern = "t_aboveground_biomass_ha_2000"

# Annual Hansen loss tiles (2001-2022)
loss_s3_path = 's3://gfw2-data/forest_change/hansen_2022/'
loss_s3_pattern = 'GFW2022'

###################################
#TODO: DO WE NEED THESE VARIABLES ANYWHERE?
#version = '1.3.1'
#version_filename = version.replace('.', '_')
#gain_years = 20
#canopy_threshold = 30
#pattern_model_extent = 'model_extent'
#model_extent_dir = os.path.join(s3_base_dir, 'model_extent/standard/20231114/')