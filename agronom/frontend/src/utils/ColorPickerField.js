import { withStyles, Paper, InputLabel } from "@material-ui/core";
import { TwitterPicker } from "react-color";
import React from "react";

const styles = theme => ({
  root: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    marginTop: 16,
    fontSize: 16
  },
  popover: {
    position: "absolute",
    zIndex: "999",
    top: 145,
    right: 165
  },
  cover: {
    position: "fixed",
    top: 0,
    right: 0,
    bottom: 0,
    left: 0
  }
});

function createStyled(styles, options) {
  function Styled(props) {
    const { children, ...other } = props;
    return children(other);
  }
  return withStyles(styles, options)(Styled);
}

class ColorPickerField extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      show: false,
      color: props.field.value
    };
  }

  clickPreview = () => {
    this.setState({ show: this });
  };

  handleClose = () => {
    this.setState({ show: false });
  }

  onChangeComplete = (color, event) => {
    this.setState({color: color.hex})
    this.props.field.onChange({target: {name: 'color', value: color.hex}});
  };

  render() {
    const { classes } = this.props;
    const { color } = this.state;
    const PreviewStyled = createStyled({
      root: {
        background: color,
        marginTop: 5,
        width: 75,
        height: 25
      }
    });

    return (
      <div className={classes.root}>
        <InputLabel shrink>Цвет</InputLabel>
        <PreviewStyled>
          {({ classes }) => (
            <Paper classes={classes} onClick={this.clickPreview} />
          )}
        </PreviewStyled>
        {this.state.show && (
          <div className={classes.popover}>
            <div className={classes.cover} onClick={this.handleClose} />
            <TwitterPicker
              triangle="top-right"
              color={color}
              onChange={this.onChange}
              onChangeComplete={this.onChangeComplete}
            />
          </div>
        )}
      </div>
    );
  }
}

export default withStyles(styles)(ColorPickerField);
