export enum AssetCommand {
    create = 'create/',
    delete = 'delete/',
    edit = 'edit/',
    view = 'view/',
    detailView = 'detailView/',
    search = 'search/',
    GET_ALL_MODELS = 'assistedmodel/',
    GET_ALL_OWNERS = 'assistedowner/',
    GET_ALL_DATACENTERS = 'assisteddatacenter/',
    GET_ALL_HOSTNAME = 'assistedhostname/',
    UPLOAD_FILE = 'import/',
    EXPORT_FILE = 'export/',
    GET_NEXT_ASSET_NUM = 'nextAssetNumber/',
    GET_NETWORK_NEIGHBORHOOD = "networkNeighborhood/",
    CHANGE_PLAN_CREATE = 'createplan/',
    CHANGE_PLAN_DELETE = 'deleteplan/',
    CHANGE_PLAN_EDIT = 'editplan/',
    CHANGE_PLAN_EXECUTE = 'execute/',
    CHANGE_PLAN_GET_PLANS = 'getplans/',
    CHANGE_PLAN_CREATE_ACTION = 'createaction/',
    CHANGE_PLAN_EDIT_ACTION = 'editaction/',
    CHANGE_PLAN_DELETE_ACTION = 'deleteaction/',
    CHANGE_PLAN_GET_ACTIONS = 'getactions/',
    GENERATE_LABELS = 'labelgen/',
    DECOMMISSION = "decommission_asset/",
}
