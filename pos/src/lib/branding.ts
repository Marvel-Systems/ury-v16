export interface POSBrand {
  name: string;
  logo: string;
  favicon: string;
  logo_background?: string;
}

interface FrappeWindow extends Window {
  frappe?: {
    boot?: {
      ury_brand?: Partial<POSBrand>;
    };
  };
}

const DEFAULT_BRAND: POSBrand = {
  name: 'URY POS',
  logo: '/assets/ury/pos/ury_pos.png',
  favicon: '/ury.ico',
};

export function getPOSBrand(): POSBrand {
  const configured = (window as FrappeWindow).frappe?.boot?.ury_brand;
  return { ...DEFAULT_BRAND, ...configured };
}

export function applyBranding(): void {
  const brand = getPOSBrand();
  document.title = brand.name;

  const favicon = document.querySelector<HTMLLinkElement>('link[rel="icon"]');
  if (favicon) favicon.href = brand.favicon;
}
