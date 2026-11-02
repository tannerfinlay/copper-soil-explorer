import styles from "../styles/Header.module.css";

type Props = { className?: string };

export function Header({ className }: Props) {
  return (
    <header className={`${styles.panel} ${className}`}>
      <h1 className={styles.title}>Copper Soil Explorer</h1>
      <div>Dropdown</div>
      <div className={styles.aboutSection}>
        <button className={styles.aboutButton} onClick={() => {}}>
          About
        </button>
        <a href="https://github.com/tannerfinlay/copper-soil-explorer">Code</a>
      </div>
    </header>
  );
}
