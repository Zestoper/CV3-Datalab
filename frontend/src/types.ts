export interface Broadcast {
  id: string;
  platform_name: string;
  title: string;
  category: string | null;
  datetime_start: string;
  product_cnt: number;
  visit_cnt: number | null;
  sales_cnt: number | null;
  sales_amt: number | null;
}

export type BroadcastType = "lb" | "hs";
