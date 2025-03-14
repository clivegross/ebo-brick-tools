from enum import Enum

class EquipmentColumns(Enum):
    ID = "Id"
    RDF_LABEL = "rdf_label"
    EQUIPMENT_TYPE = "EQUIPMENT TYPE"
    RDF_TYPE = "rdf_type"
    BRICK_HAS_LOCATION = "brick_hasLocation"
    BRICK_FEEDS = "brick_feeds"
    BRICK_IS_PART_OF = "brick_isPartOf"
    BRICK_IS_FED_BY = "brick_isFedBy"
    EBO_PATH = "EBO_path"
    ALT_NAME = "ALT NAME"
    NAME_ON_SUBSYSTEM = "NAME ON SUBSYSTEM"

class PointColumns(Enum):
    POINT_NAME = "point_name"
    RDFS_LABEL = "rdfs:label"
    BLDG = "bldg"
    RDF_TYPE = "rdf:type"
    BRICK_HAS_UNIT = "brick:hasUnit"
    EBO_PATH = "nsp:hasPath"
    EQUIPMENT_TYPE = "EQUIPMENT TYPE"
    EQUIPMENT_RDF_TYPE = "equipment_rdf:type"
    IS_IN_MODEL = "in semantic model"

equipment_columns_to_include = [
    EquipmentColumns.ID.value,
    EquipmentColumns.RDF_LABEL.value,
    EquipmentColumns.EQUIPMENT_TYPE.value,
    EquipmentColumns.RDF_TYPE.value,
    EquipmentColumns.BRICK_HAS_LOCATION.value,
    EquipmentColumns.BRICK_FEEDS.value,
    EquipmentColumns.BRICK_IS_PART_OF.value,
    EquipmentColumns.BRICK_IS_FED_BY.value,
    EquipmentColumns.EBO_PATH.value,
    EquipmentColumns.ALT_NAME.value,
    EquipmentColumns.NAME_ON_SUBSYSTEM.value,
]

points_columns_to_include = [
    PointColumns.POINT_NAME.value,
    PointColumns.RDFS_LABEL.value,
    PointColumns.BLDG.value,
    PointColumns.RDF_TYPE.value,
    PointColumns.BRICK_HAS_UNIT.value,
    PointColumns.EBO_PATH.value,
    PointColumns.EQUIPMENT_TYPE.value,
    PointColumns.EQUIPMENT_RDF_TYPE.value,
]
