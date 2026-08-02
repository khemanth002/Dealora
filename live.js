(async function(){
  try{
    const response=await fetch("./deals.json?ts="+Date.now());
    if(!response.ok)return;
    const payload=await response.json();
    if(!Array.isArray(payload.deals)||!payload.deals.length)return;
    const baseRender=render;
    render=function(){
      baseRender();
      document.querySelectorAll(".deal").forEach((card,index)=>{
        const deal=filtered[index]; if(!deal)return;
        const link=card.querySelector(".buttons a"); if(link&&deal.url)link.href=deal.url;
        const art=card.querySelector(".art"),emoji=card.querySelector(".emoji");
        if(deal.image&&art&&emoji){
          emoji.innerHTML="";
          const image=document.createElement("img");
          image.src=deal.image;image.alt=deal.title;image.loading="lazy";
          image.style.cssText="width:100%;height:100%;object-fit:cover;position:absolute;inset:0";
          image.onerror=()=>{image.remove();emoji.textContent="🔥"};
          art.prepend(image);
        }
      });
    };
    D.splice(0,D.length,...payload.deals);
    render();
    const stamp=document.createElement("p");
    stamp.className="note";
    stamp.textContent="Live public feeds • Updated "+new Date(payload.updatedAt).toLocaleString();
    document.querySelector(".head").after(stamp);
  }catch(error){console.warn("Live feeds unavailable; showing curated fallback.",error)}
})();
