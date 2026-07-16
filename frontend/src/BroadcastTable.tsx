import type { Broadcast } from "./types";

function formatCount(value: number | null): string {
  return value === null ? "🔒 로그인" : value.toLocaleString();
}

function BroadcastTable({ broadcasts }: { broadcasts: Broadcast[] }) {
  return (
    <table>
      <thead>
        <tr>
          <th className="rank"></th>
          <th>방송정보</th>
          <th>분류</th>
          <th>방송시간</th>
          <th>조회수</th>
          <th>판매량</th>
          <th>매출액</th>
          <th>상품수</th>
        </tr>
      </thead>
      <tbody>
        {broadcasts.map((b, index) => (
          <tr key={b.id}>
            <td className="rank">{index + 1}</td>
            <td className="info">
              <div className="title">{b.title}</div>
              <div className="platform-name">{b.platform_name}</div>
            </td>
            <td>{b.category ?? ""}</td>
            <td>{b.datetime_start}</td>
            <td>{formatCount(b.visit_cnt)}</td>
            <td>{formatCount(b.sales_cnt)}</td>
            <td>{formatCount(b.sales_amt)}</td>
            <td>{b.product_cnt}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default BroadcastTable;
