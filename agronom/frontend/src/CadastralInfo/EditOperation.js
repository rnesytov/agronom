import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogActions,
  Button,
  DialogContent,
  TextField,
  FormControlLabel,
  Checkbox,
  FormGroup,
  Typography,
  Chip,
  IconButton,
  withStyles
} from "@material-ui/core";
import AddIcon from "@material-ui/icons/Add";
import DeleteForeverIcon from "@material-ui/icons/DeleteForever";
import { DateTimePicker, MuiPickersUtilsProvider } from "material-ui-pickers";
import MomentUtils from "@date-io/moment";
import * as moment from "moment";

const styles = theme => ({
  marginRight: {
    marginRight: theme.spacing.unit
  },
  chip: {
    marginTop: theme.spacing.unit
  },
  deleteButton: {
    marginTop: 20
  }
});

class EditOperation extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      operation: props.operation
    };
  }

  handleChangeName = event => {
    let operation = this.state.operation;
    operation.name = event.target.value;

    this.setState({ operation });
  };

  handleChangeState = event => {
    let operation = this.state.operation;
    operation.state = event.target.checked ? 0 : 1;

    this.setState({ operation });
  };

  handleChangeDate = date => {
    let operation = this.state.operation;
    operation.date = date.format();

    this.setState({ operation });
  };

  handleSubmit = event => {
    event.preventDefault();
    this.props.handleSubmit(this.state.operation);
  };

  addParameter = () => {
    let operation = this.state.operation;
    operation.parameters.push({ name: null, value: null });

    this.setState({ operation });
  };

  handleChangeParamName = (idx, event) => {
    let operation = this.state.operation;
    operation.parameters[idx].name = event.target.value;

    this.setState({ operation });
  };

  handleChangeParamValue = (idx, event) => {
    let operation = this.state.operation;
    operation.parameters[idx].value = event.target.value;

    this.setState({ operation });
  };

  removeParameter = (idx) => {
    let operation = this.state.operation;
    operation.parameters.splice(idx, 1)

    this.setState({ operation });
  }

  render() {
    const { classes, handleClose, handleDelete } = this.props;
    const { operation } = this.state;
    return (
      <Dialog open={true} onClose={handleClose}>
        <form noValidate autoComplete="off" onSubmit={this.handleSubmit}>
          <DialogTitle>Редактирование операции по полю</DialogTitle>
          <DialogContent>
            <TextField
              name="name"
              label="Имя операции"
              value={operation.name}
              onChange={this.handleChangeName}
              margin="normal"
              className={classes.marginRight}
            />
            <MuiPickersUtilsProvider utils={MomentUtils}>
              <DateTimePicker
                margin="normal"
                ampm={false}
                value={moment(operation.date)}
                name="date"
                label="Время операции"
                onChange={this.handleChangeDate}
                format="D.M.YYYY H:m"
              />
            </MuiPickersUtilsProvider>
            <FormGroup row>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={operation.state === 0}
                    onChange={this.handleChangeState}
                    name="state"
                  />
                }
                label="Выполнено"
              />
            </FormGroup>
            <Typography component="h6">Параметры операции</Typography>
            {operation.parameters.map((p, i) => (
              <React.Fragment>
                <TextField
                  name={`parameter_${i}_name`}
                  label="Параметр"
                  value={p.name}
                  margin="normal"
                  onChange={e => {
                    this.handleChangeParamName(i, e);
                  }}
                  className={classes.marginRight}
                />
                <TextField
                  name={`parameter_${i}_value`}
                  label="Значение"
                  margin="normal"
                  value={p.value}
                  onChange={e => {
                    this.handleChangeParamValue(i, e);
                  }}
                />
                <IconButton
                  className={classes.deleteButton}
                  onClick={() => {
                    this.removeParameter(i);
                  }}
                >
                  <DeleteForeverIcon />
                </IconButton>
                <br />
              </React.Fragment>
            ))}
            <br />
            <Chip
              label="Добавить параметр"
              clickable
              className={classes.chip}
              color="primary"
              icon={<AddIcon />}
              variant="outlined"
              onClick={this.addParameter}
            />
          </DialogContent>
          <DialogActions>
            <Button color="primary" variant="contained" type="submit">
              Сохранить
            </Button>
            {operation.id && (
              <Button
                color="secondary"
                variant="contained"
                onClick={() => {
                  handleDelete(operation.id);
                }}
              >
                Удалить
              </Button>
            )}
          </DialogActions>
        </form>
      </Dialog>
    );
  }
}

export default withStyles(styles)(EditOperation);
