import { AppBar, CssBaseline, withStyles, Toolbar, IconButton, Link } from "@material-ui/core";
import ExitIcon from "@material-ui/icons/ExitToApp";
import React from "react";
import { BrowserRouter as Router, Route, Link as RouterLink } from "react-router-dom";
import CadastralInfo from "../CadastralInfo";
import ListCadastrals from "../ListCadastrals";

const styles = theme => ({
  root: {
    display: "flex"
  },
  toolbar: {
    paddingRight: 24
  },
  toolbarIcon: {
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-end",
    padding: "0 8px",
    ...theme.mixins.toolbar
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen
    })
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 36
  },
  menuButtonHidden: {
    display: "none"
  },
  title: {
    flexGrow: 1,
    textDecoration: "none",
    color: "unset"
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    height: "100vh",
    overflow: "auto"
  },
  h5: {
    marginBottom: theme.spacing.unit * 2
  }
});

class Dashboard extends React.Component {
  render() {
    const { classes } = this.props;

    return (
      <Router>
        <div className={classes.root}>
          <CssBaseline />
          <AppBar position="absolute" className={classes.appBar}>
            <Toolbar className={classes.toolbar}>
              <Link
                component={RouterLink}
                variant="h6"
                color="inherit"
                noWrap
                className={classes.title}
                to="/"
                style={{ textDecoration: "none", color: "unset" }}
              >
                Agronom
              </Link>
              <div className={classes.toolbarIcon}>
                <IconButton color="inherit" href="/accounts/logout/">
                  <ExitIcon />
                </IconButton>
              </div>
            </Toolbar>
          </AppBar>
          <main className={classes.content}>
            <div className={classes.appBarSpacer} />
            <Route path="/" exact component={ListCadastrals} />
            <Route path="/:id/" component={CadastralInfo} />
          </main>
        </div>
      </Router>
    );
  }
}

export default withStyles(styles)(Dashboard);
