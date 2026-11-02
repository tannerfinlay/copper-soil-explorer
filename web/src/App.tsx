import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { MapView } from "./components/MapView";
import { StatusBar } from "./components/StatusBar";
import styles from "./styles/App.module.css";

function App() {
  return (
    <div className={styles.app}>
      <Header className={styles.header} />
      <Sidebar className={styles.sidebar} />
      <MapView className={styles.map} />
      <StatusBar className={styles.status} />
    </div>
  );
}

export default App;
