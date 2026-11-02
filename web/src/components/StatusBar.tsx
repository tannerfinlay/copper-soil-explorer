import styles from "../styles/StatusBar.module.css";

type Props = { className?: string };

export function StatusBar({ className }: Props) {
  return (
    <footer className={`${styles.panel} ${className ?? ""}`}>
      <div className="value">34.512°N 111.204°W</div>
      <div className={styles.values}>
        <div className="label">Predicted Cu</div>
        <div className="value">## mg/kg (95% ##-## mg/kg)</div>
      </div>
    </footer>
  );
}
