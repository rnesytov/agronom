import {
  Button, Card, CardActions, CardContent, Dialog, DialogActions, DialogContent,
  DialogTitle, Fab, Grid, withStyles, TextField, Typography
} from "@material-ui/core";
import AddIcon from "@material-ui/icons/Add";
import axios from "axios";
import React from "react";
import { Link } from "react-router-dom";
import LoadingState from "./LoadingState"

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

class CadastralsList extends React.Component {
  state = {
    cadastrals: [],
    addCadastralOpen: false
  };

  constructor(props) {
    super(props);

    this.input = React.createRef();
  }

  loadCadastrals() {
    axios.get("/api/v0_1/cadastral/").then(res => {
      const cadastrals = res.data;
      this.setState({ cadastrals });
    });
  }

  componentDidMount() {
    this.loadCadastrals();
  }

  showAddCadastral = () => {
    this.setState({ addCadastralOpen: true });
  };

  handleClose = () => {
    this.setState({ addCadastralOpen: false });
  };

  handleAddCadastral = () => {
    const cadNumber = this.input.current.value;

    axios
      .post("/api/v0_1/cadastral/", { cadastral_number: cadNumber })
      .then(res => {
        this.loadCadastrals();
      });

    this.handleClose();
  };

  render() {
    const { classes } = this.props;
    const { cadastrals } = this.state;

    let content;
    if (cadastrals.length === 0) {
      content = <span>Нет кадастровых учатсков</span>;
    } else {
      content = cadastrals.map(cad => (
        <Grid key={cad.id} item>
          <Card className={classes.card}>
            <CardContent>
              <Typography
                className={classes.title}
                color="textSecondary"
                gutterBottom
              >
                Кадастровый номер
              </Typography>
              <Typography variant="h5" component="h2">
                {cad.cadastral_number}
              </Typography>
              <LoadingState loadingState={cad.loading_state}/>
            </CardContent>
            <CardActions>
              <Button
                size="small"
                component={Link}
                to={"/" + cad.id + "/"}
                disabled={cad.loading_state !== 1}
              >
                Поля
              </Button>
            </CardActions>
          </Card>
        </Grid>
      ));
    }

    return (
      <Grid container spacing={40}>
        {content}
        <Fab
          color="primary"
          aria-label="Add"
          className={classes.fab}
          onClick={this.showAddCadastral}
        >
          <AddIcon />
        </Fab>
        <Dialog
          open={this.state.addCadastralOpen}
          onClose={this.handleClose}
          aria-labelledby="form-dialog-title"
        >
          <DialogTitle id="form-dialog-title">
            Добавление кадастрового участка
          </DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              id="cadastral_number"
              label="Кадастроый номер"
              type="text"
              inputRef={this.input}
              fullWidth
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Закрыть
            </Button>
            <Button onClick={this.handleAddCadastral} color="primary">
              Добавить
            </Button>
          </DialogActions>
        </Dialog>
      </Grid>
    );
  }
}

export default withStyles(styles)(CadastralsList);
