import { MapContainer, TileLayer, ZoomControl } from "react-leaflet";
type Props = { className?: string };

export function MapView({ className }: Props) {
  return (
    <main className={className}>
      <MapContainer
        preferCanvas={true}
        center={[39.8283, -98.5795]}
        zoom={5}
        zoomControl={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url={`https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png?key=${import.meta.env.VITE_CARTO_KEY}`}
          subdomains="abcd"
          maxZoom={20}
        />
        <ZoomControl position="topright" />
      </MapContainer>
    </main>
  );
}
