select display_data_name, wms_catalogue_id from metadata.display_catalogue;

update metadata.display_catalogue set wms_catalogue_id = 1 where display_data_name = 'freshwater_atlas_glaciers';

update metadata.display_catalogue set wms_catalogue_id = NULL where display_data_name = 'cadastral';

select * from metadata.wms_catalogue where wms_catalogue_id = 1;
select * from metadata.wms_catalogue;
select * from metadata.wms_catalogue where wms_catalogue_id = 3
update metadata.wms_catalogue set wms_style = '719' where wms_name = 'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY';
UPDATE metadata.wms_catalogue set wms_style = '4883' where wms_name = 'WHSE_WILDLIFE_MANAGEMENT.WCP_CRITICAL_HABITAT_SP';