import React from 'react';
import Modal from '@material-ui/core/Modal';
import TextField from "@material-ui/core/TextField";
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import { palette } from '@material-ui/system';

export default class DetailedView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            showConfirmationBox:false,
        };

        this.closeModal = this.closeModal.bind(this);
        this.confirmDelete = this.confirmDelete.bind(this);
        this.deleteItem = this.deleteItem.bind(this);
    }

    confirmDelete() {
        this.setState({ showConfirmationBox: true });
    }

    closeModal() {
        this.setState({showConfirmationBox:false,});
    }

    deleteItem() {
        this.setState({ showConfirmationBox: false });
        this.props.delete();
    }

    render() {
        return (
        <div>
            <Modal
                style={{top: `50%`,left: `50%`,transform: `translate(-50%, -50%)`, backgroundColor: palette.background.paper,}}
                aria-labelledby="simple-modal-title"
                aria-describedby="simple-modal-description"
                open={this.props.showDetailedView}
                onClose={this.props.closeDetailedView}
            >
                {
                this.props.loading ? <CircularProgress /> :
                <div>
                    {this.props.inputs.map(input => (
                        <TextField name={input} disabled={this.props.disabled} id="standard-basic" label={input} onChange={this.props.updateModelEdited} defaultValue={this.props.defaultValues[input]}/>
                    ))}
                    {this.props.disabled ? null:
                    <div>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={this.props.edit}
                            disabled={this.state.showConfirmationBox}
                        >
                            Save
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={this.confirmDelete}
                            disabled={this.state.showConfirmationBox}
                        >
                            Delete
                        </Button>
                    </div>}
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={this.props.closeDetailedView}
                            disabled={this.state.showConfirmationBox}
                        >
                            Close
                        </Button>

                    {this.state.showConfirmationBox ? <div>
                        Are you sure you wish to delete?
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={this.deleteItem}
                        >
                            Yes
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={this.closeModal}
                        >
                            No
                        </Button>
                    </div>:null}
                </div>}
            </Modal>
        </div>
        );
    }
}
