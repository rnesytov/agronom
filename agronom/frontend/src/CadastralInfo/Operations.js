import React from "react";
import axios from "axios";
import {
  List,
  ListItem,
  Fab,
  withStyles,
  ListItemText
} from "@material-ui/core";
import AddIcon from "@material-ui/icons/Add";
import * as moment from "moment";
import EditOperation from "./EditOperation";

const styles = theme => ({
  card: {
    minWidth: 275
  },
  fab: {
    position: "absolute",
    bottom: 25,
    right: 25
  }
});

class Operations extends React.Component {
  state = {
    operations: [],
    editOperationOpen: false,
    currenteOperation: null
  };

  loadOperations() {
    axios
      .get("/api/v0_1/operations/", {
        params: { field_id: this.props.field.id }
      })
      .then(res => {
        this.setState({ operations: res.data });
      });
  }

  componentDidMount() {
    this.loadOperations();
  }

  showEditOperation = operation => {
    this.setState({ editOperationOpen: true, currenteOperation: operation });
  };

  handleClose = () => {
    this.setState({
      editOperationOpen: false,
      currenteOperation: null
    });
  };

  handleSubmit = operation => {
    let method;

    if (operation.id){
      method = axios.put
    } else {
      method = axios.post
    }

    method("/api/v0_1/operations/", operation).then(() => {
      this.handleClose();
      this.loadOperations();
    });
  };

  handleDelete = id => {
    axios.delete("/api/v0_1/operations/", {data: {id: id}}).then(() => {
      this.handleClose();
      this.loadOperations();
    });
  }

  showAddOperation = () => {
    this.setState({
      currenteOperation: {
        id: null,
        field_id: this.props.field.id,
        date: moment().format(),
        state: 1,
        parameters: [],
        name: ""
      },
      editOperationOpen: true
    });
  }

  render() {
    const { classes } = this.props;
    return (
      <React.Fragment>
        {this.state.operations.length === 0 && (
          <span>Нет операций по полю</span>
        )}
        <List>
          {this.state.operations.map((o, i) => (
            <ListItem
              key={i}
              button
              onClick={() => {
                this.showEditOperation(o);
              }}
            >
              <ListItemText
                primary={o.name}
                secondary={moment(o.date).format("D.M.YYYY")}
              />
            </ListItem>
          ))}
        </List>
        <Fab
          color="primary"
          aria-label="Add"
          className={classes.fab}
          onClick={this.showAddOperation}
        >
          <AddIcon />
        </Fab>
        {this.state.editOperationOpen && (
          <EditOperation
            operation={this.state.currenteOperation}
            handleClose={this.handleClose}
            handleSubmit={this.handleSubmit}
            handleDelete={this.handleDelete}
          />
        )}
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(Operations);
