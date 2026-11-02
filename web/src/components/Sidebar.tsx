import styles from "../styles/Sidebar.module.css";

type Props = { className?: string };

export function Sidebar({ className }: Props) {
  return (
    <aside className={`${styles.panel} ${className}`}>
      <section className={styles.form}>
        <div>
          <h2 className={styles.panelHeader}>Map layer</h2>
          <hr></hr>
        </div>
        <div>
          <h2 className={styles.panelHeader}>Copper in topsoil</h2>
          <hr></hr>
        </div>
        <div>
          <h2 className={styles.panelHeader}>Legend</h2>
          <hr></hr>
        </div>
        <div>
          <h2 className={styles.panelHeader}>Model</h2>
        </div>
      </section>
      <section className={`caption ${styles.dataCitation}`}>
        Data: USGS Data Series 801 (Smith et al., 2013)
      </section>
    </aside>
  );
}
