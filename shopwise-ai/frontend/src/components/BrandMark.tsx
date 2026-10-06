export function BrandMark() {
  return <div className="brand-mark" aria-label="ShopWise AI">
    <div className="brand-symbol" aria-hidden="true"><span></span><span></span></div>
    <div><div className="brand-name">ShopWise <b>AI</b></div><div className="brand-eyebrow">Research agent</div></div>
    <style>{`.brand-mark{display:flex;align-items:center;gap:10px}.brand-symbol{position:relative;width:28px;height:26px}.brand-symbol span{position:absolute;width:18px;height:18px;border-top:3px solid #0f766e;border-right:3px solid #0f766e;transform:rotate(45deg);top:3px}.brand-symbol span:first-child{left:1px}.brand-symbol span:last-child{left:9px;opacity:.45}.brand-name{font:800 18px/1 Manrope,sans-serif;letter-spacing:-.04em}.brand-name b{color:#0f766e}.brand-eyebrow{color:#69757e;font:700 9px/1.7 Manrope,sans-serif;letter-spacing:.16em;text-transform:uppercase}`}</style>
  </div>
}
