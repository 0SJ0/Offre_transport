import streamlit as st
from PIL import Image

global_css="""
<style>
[data-testid="stAppViewContainer"]{
opacity: 1;
#font : oblique 14px Arial, Helvetica, sans-serif;
background-image: url("https://tof.cx/images/2017/09/07/d5511f292f636eb69e66eddf9236d333.gif");
background-repeat: no-repeat;
background-size: 2000px 900px;
}
[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}
[data-testid="stToolbar"]{
background-color: rgba(0,0,0,0);
}

</style>
"""
#[data-testid="stSidebar"]{
#color: blue;
#opacity: 0.8;
#); #background-image: url("https://www.vidaxl.fr/dw/image/v2/BFNS_PRD/on/demandware.static/-/Sites-vidaxl-catalog-master-sku/default/dw20116bde/hi-res/536/696/2334/440418/image_2_440418.jpg?sw=400"
#}


st.markdown(global_css,unsafe_allow_html=True)

#st.sidebar.markdown("<footer><p style='text-align:center;'> <img src='https://upload.wikimedia.org/wikipedia/fr/thumb/2/2e/R%C3%A9gion_Hauts-de-France_logo_2016.svg/1200px-R%C3%A9gion_Hauts-de-France_logo_2016.svg.png' width='100' height='100'> </p></footer>", unsafe_allow_html=True)




