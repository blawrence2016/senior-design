import React from 'react';

import axios from 'axios';

import Grid from '@material-ui/core/Grid';

import { AssetCommand } from '../enums/AssetCommands.ts'
import { AssetInput } from '../enums/AssetInputs.ts'
import { Privilege } from '../../enums/privilegeTypes.ts'
import ImpExpAsset from '../helpers/ImpExpAsset';
import FilterAsset from '../helpers/FilterAsset';
import getURL from '../../helpers/functions/GetURL';
import DetailAsset from '../helpers/DetailsAsset';
import CreateAsset from '../helpers/CreateAsset';
import StatusDisplay from '../../helpers/StatusDisplay';
import TableView from '../../helpers/TableView';
import ErrorBoundary from '../../errors/ErrorBoundry';
import * as AssetConstants from "../AssetConstants";
import "../stylesheets/AssetStyles.css";

const columns = [
    'model',
    'hostname',
    'rack',
    'rack_position',
]

export default class AssetsView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tableItems:[],

            statusSeverity:'',
            statusMessage:'',

            detailStatusOpen:false,
            detailStatusSeverity:'',
            detailStatusMessage:'',

            deleteAssetRack:'',
            deleteAssetrack_position:'',
            viewAssetRack:'',
            viewAssetrack_position:'',

            showDetailedView: false,
            detailViewLoading:false,
            detailedValues : null,
            originalRack:'',
            originalrack_position:'',
        };

        axios.defaults.headers.common['token'] = this.props.token;
        axios.defaults.headers.common['privilege'] = this.props.privilege;

    }

    componentDidMount() {

    }

    editAsset = () => {
        let body = this.state.detailedValues.getAssetAsJSON();
        body[AssetInput.RACK_ORIGINAL] = this.state.originalRack;
        body[AssetInput.RACK_U_ORIGINAL] = this.state.originalrack_position;
        axios.post(
            getURL(AssetConstants.ASSETS_MAIN_PATH, AssetCommand.edit),body
            ).then(response => {
                if (response.data.message === AssetConstants.SUCCESS_TOKEN) {
                    this.setState({
                        showStatus: true,
                        statusMessage: "Successfully edited asset",
                        statusSeverity:AssetConstants.SUCCESS_TOKEN,
                        detailedValues : null,
                        showDetailedView:false,
                    });
                } else {
                    this.setState({ detailStatusOpen: true, detailStatusMessage: response.data.message, detailStatusSeverity:AssetConstants.ERROR_TOKEN })
                }
            });
    }


    deleteAsset = () => {
        var body = {};
        body[AssetInput.RACK] = this.state.originalRack;
        body[AssetInput.RACK_U] = this.state.originalrack_position;

        axios.post(
            getURL(AssetConstants.ASSETS_MAIN_PATH, AssetCommand.delete), body
            ).then(response => {
                if (response.data.message === AssetConstants.SUCCESS_TOKEN) {
                    this.setState({
                        showStatus: true,
                        statusMessage: "Successfully deleted asset",
                        statusSeverity:AssetConstants.SUCCESS_TOKEN,
                        originalRack:'',
                        originalrack_position:'',
                        showDetailedView:false
                    });
                } else {
                    this.setState({ showStatus: true, statusMessage: response.data.message, statusSeverity:AssetConstants.ERROR_TOKEN })
                }
            });
    }

    detailViewAsset = (rack, rack_position) => {
        var body = {};
        body[AssetInput.RACK] = rack;
        body[AssetInput.RACK_U] = rack_position;

        axios.post(
            getURL(AssetConstants.ASSETS_MAIN_PATH, AssetCommand.detailView), body
            ).then(response => this.setState({ detailedValues: response.data['assets'][0], detailViewLoading:false})
            );

        this.setState({
            viewAssetRack:'',
        });
    }



    showDetailedView = (id) => {
        this.setState({
            showDetailedView: true,
            detailViewLoading:true,
            originalRack: this.state.items[id][AssetInput.RACK],
            originalrack_position: this.state.items[id][AssetInput.RACK_U],
        });

        var rack = this.state.items[id][AssetInput.RACK];
        var rack_position = this.state.items[id][AssetInput.RACK_U];

        this.detailViewAsset(rack, rack_position);
    }

    closeDetailedView = () => {
        this.setState({ showDetailedView: false })
    }

    updateAssetEdited = (event) => {
        this.state.detailedValues.updateVal(event.target.value);
        this.forceUpdate()
    }

    closeShowStatus = () => {
        this.setState({ showStatus: false })
    }

    detailStatusClose = () => {
        this.setState({ detailStatusOpen: false })
    }

    render() {
        return (
            <div>
                <ErrorBoundary>
                        <StatusDisplay
                            open={this.state.showStatus}
                            severity={this.state.statusSeverity}
                            closeStatus={this.closeShowStatus}
                            message={this.state.statusMessage}
                        />
                        <Grid container spacing={3}>
                                <Grid item xs={12}>
                                    <FilterAsset
                                        search={this.search}
                                        filters={columns}
                                    />
                                </Grid>
                                <Grid item xs={3}>
                                    {(this.props.privilege === Privilege.ADMIN) ?
                                    <CreateAsset
                                        search={this.search}
                                    />:null}
                                </Grid>
                                <Grid item xs={6}>
                                    {(this.props.privilege === Privilege.ADMIN) ?
                                    <ImpExpAsset
                                        downloadTable={this.downloadTable}
                                    />:null}
                                </Grid>
                                <Grid item xs={12}>
                                    <TableView
                                        columns={columns}
                                        vals={this.state.tableItems}
                                        keys={columns}
                                        showDetailedView={this.showDetailedView}
                                        filters={columns}
                                    />
                                    <DetailAsset
                                        statusOpen={this.state.detailStatusOpen}
                                        statusSeverity={this.state.detailStatusSeverity}
                                        statusClose={this.detailStatusClose}
                                        statusMessage={this.state.detailStatusMessage}
                                        showDetailedView={this.state.showDetailedView}
                                        closeDetailedView={this.closeDetailedView}
                                        updateModelEdited={this.updateAssetEdited}
                                        defaultValues={this.state.detailedValues}
                                        loading={this.state.detailViewLoading}
                                        edit={this.editAsset}
                                        delete={this.deleteAsset}
                                        disabled={this.props.privilege===Privilege.USER}
                                    />
                                </Grid>
                            </Grid>
                </ErrorBoundary>
            </div>
        );
    }
}
