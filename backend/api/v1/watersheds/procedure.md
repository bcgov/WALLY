# Upstream catchment areas using Freshwater Atlas and CDEM

The WALLY Surface Water Analysis feature collects and outputs a variety of water and climate data for users.  The search area for this feature is the upstream catchment area, or basin, originating from a point on a stream that the user selects.

The Freshwater Atlas (FWA) is the primary source for the catchment areas used by WALLY. However, the FWA fundamental watershed polygons (1:20000) are not small enough to accurately delineate a catchment from an arbitrary stream point, as there will always be downstream area included ([see below example](#Define-working-area-for-the-catchment)).  This document presents a method for using the catchment areas defined by the Freshwater Atlas fundamental polygons, with a refinement/correction for the area that the point of interest was placed in.

In addition to the Freshwater Atlas fundamental watersheds, the method relies on catchment delineation using a Digital Elevation Model (DEM) and the [WhiteboxTools program](https://jblindsay.github.io/ghrg/WhiteboxTools/index.html). WhiteboxTools is an open source GIS analyis program developed at the University of Guelph's Geomorphometry and Hydrogeomatics Research Group (GHRG) that is well suited for integration with other software.

The Digital Elevation Model used in this example is the CDEM 3s (90m) data.  Future plans include integrating the CDEM 0.75 arcsecond (25m) digital elevation model.

Freshwater Atlas: https://www2.gov.bc.ca/gov/content/data/geographic-data-services/topographic-data/freshwater

CDEM: https://open.canada.ca/data/en/dataset/7f245e4d-76c2-4caa-951a-45d1d2051333

WhiteboxTools: https://jblindsay.github.io/ghrg/WhiteboxTools/index.html

## Point of Interest
The user selects a point of interest along a stream.  The catchment area generated will be the area that drains to this point (i.e., is "upstream").

![010_Point_of_Interest](https://user-images.githubusercontent.com/27074993/116722983-e7d95a00-a993-11eb-871f-d1f7a065a1a2.jpg)

## Define working area for the catchment
The Freshwater Atlas datasets and CDEM data files are too large to process all at once.  We can speed up calculations and queries by defining a manageable sized "working area".

The working area is found by combining Freshwater Atlas polygons that are associated with the stream (using the FWA_WATERSHED_CODE property), starting from the next downstream tributary of the selected stream (using the LOCAL_WATERSHED_CODE property). Because we start downstream, this will always be an overestimate of the actual upstream catchment area.

![020_overestimate](https://user-images.githubusercontent.com/27074993/116723008-ec057780-a993-11eb-9f63-43cfbbfb156e.jpg)

## Retrieve a pre-processed DEM raster
A DEM raster file is retrieved from WALLY covering the working area.  This raster has been preprocessed by burning streams using WhiteBoxTools using the [FillBurn](https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#FillBurn) method described in the papers below. The purpose of burning streams is to force flow into known, mapped streams (in our case, using the Freshwater Atlas Stream Networks dataset) to correct for any discrepancies between the DEM data and the Freshwater Atlas linework.
 * Lindsay JB. 2016. The practice of DEM stream burning revisited. Earth Surface Processes and Landforms, 41(5): 658-668. DOI: 10.1002/esp.3888
 * Saunders, W. 1999. Preparation of DEMs for use in environmental modeling analysis, in: ESRI User Conference. pp. 24-30.

The Freshwater Atlas provides the vector stream source (seen below, as applied to the DEM)

![030_dem_covering_area](https://user-images.githubusercontent.com/27074993/116723029-ef98fe80-a993-11eb-9932-26fdbaf7e890.jpg)

## Flow Direction raster
A Flow direction (or "pointer") raster is produced using the D8 flow algorithm as implemented in the [WhiteboxTools D8Pointer routine](https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#D8Pointer).

![040_flow_direction](https://user-images.githubusercontent.com/27074993/116723051-f1fb5880-a993-11eb-820c-6545bcf7da8b.jpg)

## Flow Accumulation raster
A Flow Accumulation raster is produced, also using the D8 algorithm as implemented in the [WhiteboxTools D8FlowAccumulation routine](https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#D8FlowAccumulation).

![050_flow_accumulation](https://user-images.githubusercontent.com/27074993/116723062-f3c51c00-a993-11eb-8dce-2735aca71199.jpg)

## Snap point to Flow Accumulation streamline

Although the user selected a point on or near a stream, it's important that the DEM delineation function start from a grid cell containing the flow accumulation corresponding to that stream (in other words, it has to hit the exact pixel that the stream flows through).  In the below example, the user point (yellow) is corrected to touch the accumulation area (purple) using the [SnapPourPoints routine](https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#SnapPourPoints).

Note: the snapped pour point always tends to be downstream of the selected point. More info is at the above link.

![060_snapped_point](https://user-images.githubusercontent.com/27074993/116723081-f58edf80-a993-11eb-82b0-56d5dc3f5995.jpg)

## Delineate watershed

Using the Flow direction raster and the snapped point, the watershed can be delineated with [WhiteboxTools Watershed](https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#Watershed).

![070_delineated_watershed](https://user-images.githubusercontent.com/27074993/116723092-f758a300-a993-11eb-88aa-8c0174d3ff6d.jpg)

## Apply DEM delineated watershed to Freshwater Atlas

The polygon may not correspond exactly to the Freshwater Atlas linework.  We want to use the Freshwater Atlas linework everywhere upstream of the point.

![090_dem_plus_linework](https://user-images.githubusercontent.com/27074993/116723111-ff184780-a993-11eb-88fd-53825dcb5d10.jpg)

To achieve this, we again use the Freshwater Atlas fundamental watersheds, but this time we exclude the polygon that the user's point of interest is within (or is very close to, as some large rivers have several side-by-side polygons covering the river width as well as face unit polygons).   We can then fill in the missing area from the point of interest to the first upstream fundamental watershed polygon using the DEM delineated catchment (**note**: need a screenshot showing this "hybrid" watershed clearly).

![091_fwa_linework](https://user-images.githubusercontent.com/27074993/116723128-017aa180-a994-11eb-971a-a5c129785aff.jpg)


## Final result

The final result is the upstream catchment area based on the Freshwater Atlas, but refined around the point of interest using the result of the DEM delineation technique.

![111_FWA_result](https://user-images.githubusercontent.com/27074993/116723133-04759200-a994-11eb-9707-c528b8028aad.jpg)
