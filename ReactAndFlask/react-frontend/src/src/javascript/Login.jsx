import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import { makeStyles } from '@material-ui/core/styles';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';

import axios from 'axios';


function submitCredentials(username, password) {
    axios.post('http://localhost:4010/users/authenticate', { "username":username, "password":password} ).then(response => console.log(response))
}

const useStyles = makeStyles(theme => ({
    paper: {
        marginTop: theme.spacing(8),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        marginTop: theme.spacing(1),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
}));

export default function Login(props) {
    const classes = useStyles();
    return (
        <div className={classes.paper}>
            <TextField
                id="outlined-basic"
                label="Username"
                variant="outlined"
                required="true"
                ref='username'
            />
            <TextField
                id="outlined-basic"
                label="Password"
                variant="outlined"
                required="true"
                ref='password'
            />
            <FormControl className={classes.form}>
                <FormGroup>
                    <FormControlLabel
                        value="end"
                        control={<Checkbox color="primary" />}
                        label="End"
                        labelPlacement="end"
                    />
                </FormGroup>
            </FormControl>
            <Button
                onClick={() => (submitCredentials(this.refs.username.getValue(), this.refs.password.getValue()))}
                variant="contained"
                color="primary"
                className={classes.submit}
            >
                Sign In
            </Button>
        </div>
    );
}
