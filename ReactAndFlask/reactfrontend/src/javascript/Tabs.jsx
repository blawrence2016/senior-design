import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

import ModelsView from './models/pages/ModelsView';
import UsersView from './users/pages/UsersView';
import InstancesView from './instances/pages/InstancesView';
import RacksView from './racks/pages/RacksView';
import StatisticsView from './statistics/pages/StatisticsView';

import { Privilege } from './enums/privilegeTypes.ts'

import ErrorBoundry from './errors/ErrorBoundry';

export default class TabViewer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currentTabID:0,
        };
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event, newValue) {
        this.setState({ currentTabID: newValue })
    }

    render() {
        return (
        <div>
            <ErrorBoundry>
            <AppBar position="static">
                <Tabs value={this.state.currentTabID} onChange={this.handleChange}>
                    <Tab value={0} style={{flexGrow: 1,}} label="Models"> </Tab>
                    <Tab value={1} style={{flexGrow: 1,}} label="Instances" ></Tab>
                    {(this.props.privilege == Privilege.ADMIN) ? <Tab value={2} style={{flexGrow: 1,}} label="Users"></Tab> : null}
                    <Tab value={3} style={{flexGrow: 1,}} label="Racks" />
                    <Tab value={4} style={{flexGrow: 1,}} label="Statistics" />
                    <Button
                        style={{flexGrow: 1,}}
                        variant="contained"
                        color="secondary"
                        onClick={this.props.logout}
                    >
                        Logout
                    </Button>
                </Tabs>
            </AppBar>
            <Typography
                component="div"
                role="tabpanel"
                hidden={this.state.currentTabID !== 0}
                id={`simple-tabpanel-0`}
                aria-labelledby={`simple-tab-0`}
            >
                <ModelsView token={this.props.token} privilege={this.props.privilege} />
            </Typography>
            <Typography
                component="div"
                role="tabpanel"
                hidden={this.state.currentTabID !== 1}
                id={`simple-tabpanel-0`}
                aria-labelledby={`simple-tab-0`}
            >
                <InstancesView token={this.props.token} privilege={this.props.privilege} />
            </Typography>
            <Typography
                component="div"
                role="tabpanel"
                hidden={this.state.currentTabID !== 2}
                id={`simple-tabpanel-0`}
                aria-labelledby={`simple-tab-0`}
            >
                <UsersView token={this.props.token} privilege={this.props.privilege} />
            </Typography>
            <Typography
                component="div"
                role="tabpanel"
                hidden={this.state.currentTabID !== 3}
                id={`simple-tabpanel-0`}
                aria-labelledby={`simple-tab-0`}
            >
                <RacksView token={this.props.token} privilege={this.props.privilege} />
            </Typography>
            <Typography
                component="div"
                role="tabpanel"
                hidden={this.state.currentTabID !== 4}
                id={`simple-tabpanel-0`}
                aria-labelledby={`simple-tab-0`}
            >
                <StatisticsView token={this.props.token} privilege={this.props.privilege} />
            </Typography>
            </ErrorBoundry>
        </div>);
    }
}
