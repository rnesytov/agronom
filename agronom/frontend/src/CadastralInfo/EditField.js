import { Button, withStyles, Paper, InputLabel } from "@material-ui/core";
import { Formik, Form, Field } from "formik";
import { FormikTextField as TextField } from "formik-material-fields";
import ColorPickerField from "../utils/ColorPickerField"
import React from "react";

const styles = theme => ({
  formContainer: {
    display: "flex",
    flexWrap: "wrap",
    padding: 20
  },
  button: {
    margin: theme.spacing.unit,
    width: 280
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 180
  }
});

export default withStyles(styles)(function({
  classes,
  field,
  handleDelete,
  handleSubmit
}) {
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
        <Field name="color" component={ColorPickerField} />
        <br />
        <Button
          color="primary"
          variant="contained"
          className={classes.button}
          type="submit"
        >
          Сохранить
        </Button>
        <Button
          color="secondary"
          variant="contained"
          className={classes.button}
          onClick={handleDelete}
        >
          Удалить
        </Button>
      </Form>
    </Formik>
  );
});
