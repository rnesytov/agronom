import { Button, withStyles } from "@material-ui/core";
import { Formik, Form } from "formik";
import { FormikTextField as TextField } from "formik-material-fields";
import React from "react";

const styles = theme => ({
  formContainer: {
    display: "flex",
    flexWrap: "wrap",
    padding: 20
  },
  button: {
    margin: theme.spacing.unit
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200
  }
});

class EditField extends React.Component {
  render() {
    const { classes, field, handleDelete, handleSubmit } = this.props;

    return (
      <Formik initialValues={field} onSubmit={handleSubmit}>
        <Form className={classes.formContainer} autoComplete="off">
          <TextField
            margin="normal"
            label="Имя поля"
            name="name"
            className={classes.textField}
          />
          <TextField
            margin="normal"
            label="Культура"
            name="crop_type"
            className={classes.textField}
          />
          <TextField
            margin="normal"
            label="Цвет"
            name="color"
            className={classes.textField}
          />
          <br />
          <Button
            color="primary"
            variant="contained"
            fullWidth
            className={classes.button}
            type="submit"
          >
            Сохранить
          </Button>

          <Button
            color="secondary"
            variant="contained"
            fullWidth
            className={classes.button}
            onClick={handleDelete}
          >
            Удалить
          </Button>
        </Form>
      </Formik>
    );
  }
}

export default withStyles(styles)(EditField);
