import {
  Paper,
  withStyles,
  Drawer,
  AppBar,
  Tabs,
  Tab
} from "@material-ui/core";
import axios from "axios";
import L from "leaflet";
import React from "react";
import { FeatureGroup, Map, Polygon, TileLayer, GeoJSON } from "react-leaflet";
import { EditControl } from "react-leaflet-draw";
import EditField from "./EditField";
import Weather from "./Weather";
import NDVI from "./NDVI";
import Operations from "./Operations";
import ReactDistortableImageOverlay from "react-leaflet-distortable-imageoverlay";

const styles = {
  map: {
    height: "90vh"
  },
  drawer: {
    width: 640
  }
};

class CadastralInfo extends React.Component {
  state = {
    cadastral: null,
    fields: null,
    ndvi: [],

    editDrawerOpen: false,
    currentField: null,
    tabValue: 0
  };

  componentDidMount() {
    this.loadCadastral();
    this.loadFields();
  }

  loadCadastral() {
    axios
      .get(`/api/v0_1/cadastral/${this.props.match.params.id}/`)
      .then(res => {
        const cadastral = res.data;
        this.setState({ cadastral });
        document.title = `Участок ${cadastral.cadastral_number}`;
      });
  }

  loadFields() {
    axios
      .get(`/api/v0_1/cadastral/${this.props.match.params.id}/fields/`)
      .then(res => {
        const fields = res.data;
        this.setState({ fields });
      });
  }

  addField(geoJSON) {
    axios
      .post(`/api/v0_1/cadastral/${this.props.match.params.id}/fields/`, {
        polygon: geoJSON.geometry
      })
      .then(res => {
        this.loadFields();
        this.showEditDrawer(res.data);
      });
  }

  deleteField = () => {
    axios
      .delete(`/api/v0_1/cadastral/${this.props.match.params.id}/fields/`, {
        data: { id: this.state.currentField.id }
      })
      .then(() => {
        this.hideEditDrawer();
        this.loadFields();
      });
  };

  updateField = field => {
    axios
      .put(`/api/v0_1/cadastral/${this.props.match.params.id}/fields/`, field)
      .then(() => {
        this.hideEditDrawer();
        this.loadFields();
      });
  };

  showEditDrawer = field => {
    this.setState({ editDrawerOpen: true, currentField: field });
  };

  hideEditDrawer = () => {
    this.setState({ editDrawerOpen: false, currentField: {} });
  };

  getBounds = () => {
    const poly = this.state.cadastral.polygon;

    return L.geoJSON(poly).getBounds();
  };

  _onCreate = e => {
    const geoJSON = e.layer.toGeoJSON();

    this.addField(geoJSON);
  };

  handleTabChange = (event, tabValue) => {
    this.setState({ tabValue });
  };

  showNDVI = ndvi => {
    const coords = ndvi.boundary.coordinates;

    const preparedNDVI = {
      url: ndvi.img,
      bounds: [
        L.latLng(coords[0][1], coords[0][0]),
        L.latLng(coords[1][1], coords[1][0]),
        L.latLng(coords[2][1], coords[2][0]),
        L.latLng(coords[3][1], coords[3][0])
      ]
    };

    this.setState({ ndvi: this.state.ndvi.concat([preparedNDVI]) });
  };

  render() {
    const { classes } = this.props;

    if (this.state.cadastral && this.state.fields) {
      return (
        <Paper>
          <Map bounds={this.getBounds()} className={classes.map}>
            <TileLayer url="http://mt0.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}" />
            {this.state.cadastral.polygon.coordinates}
            <GeoJSON
              data={this.state.cadastral.polygon}
              fill={false}
              color="#fff"
              weight={2}
            />
            <FeatureGroup>
              <EditControl
                position="topright"
                onEdited={this._onEdit}
                onCreated={this._onCreate}
                onDeleted={this._onDelete}
                edit={{ edit: false, remove: false }}
                draw={{
                  polyline: false,
                  rectangle: false,
                  circle: false,
                  marker: false,
                  circlemarker: false,
                  polygon: {
                    allowIntersection: false,
                    shapeOptions: { weight: 1 }
                  }
                }}
              />
              {this.state.fields.map((f, idx) => (
                <Polygon
                  key={idx}
                  positions={L.GeoJSON.coordsToLatLngs(
                    f.polygon.coordinates,
                    1
                  )}
                  onclick={() => {
                    this.showEditDrawer(f);
                  }}
                  weight={1}
                  color={f.color}
                  fillOpacity={0.1}
                />
              ))}
              {this.state.ndvi.map((n, idx) => (
                <ReactDistortableImageOverlay
                  corners={n.bounds}
                  url={n.url}
                  key={idx}
                />
              ))}
            </FeatureGroup>
          </Map>
          <Drawer
            anchor="left"
            open={this.state.editDrawerOpen}
            onClose={this.hideEditDrawer}
          >
            <div className={classes.drawer}>
              <AppBar position="static">
                <Tabs
                  value={this.state.tabValue}
                  onChange={this.handleTabChange}
                >
                  <Tab label="Поле" />
                  <Tab label="Погода" />
                  <Tab label="NDVI" />
                  <Tab label="Операции" />
                </Tabs>
              </AppBar>
              {this.state.tabValue === 0 && (
                <EditField
                  field={this.state.currentField}
                  handleDelete={this.deleteField}
                  handleSubmit={this.updateField}
                />
              )}
              {this.state.tabValue === 1 && (
                <Weather field={this.state.currentField} />
              )}
              {this.state.tabValue === 2 && (
                <NDVI
                  field={this.state.currentField}
                  showNDVI={this.showNDVI}
                />
              )}
              {this.state.tabValue === 3 && (
                <Operations field={this.state.currentField} />
              )}
            </div>
          </Drawer>
        </Paper>
      );
    } else {
      return "Загрузка карты";
    }
  }
}

export default withStyles(styles)(CadastralInfo);
