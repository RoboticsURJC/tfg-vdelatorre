# Repositorio de trabajo del TFG
# Víctor de la Torre Rosa

Como primera idea, este TFG estará enfocado a domotizar una vivienda
gracias al uso de una raspberry mediante reconocimiento por voz y facial, por lo
que este asistente a parte de poder comunicarte con él,otorgará mayor seguridad 
a cualquier tipo de datos que se deseen guardar y a un coste relativamente bajo.

## Material necesario:

[Raspberry PI 4 modelo B](https://www.amazon.es/Raspberry-Modelo-Cortex-A72-1-50GHz-Bluetooth/dp/B0CJ4XHZ4G/ref=sr_1_1_sspa?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2PC3BKPDGNP9T&dib=eyJ2IjoiMSJ9.JC3sH7yAJO39e093s-s2MB6--RiRzs-pjKdtN28bw4srryrt8yXVd_wlzPO6hZgCq65K9AIH0sEG8kIDFgwSwnUxb_3y7JMFhehZRV-qRK4q7s-8fuFh4BpcBpOn1te7EJRr5AVPRmkBUKH2ti3ZGQohnMS5g0jRL4OfybnpCzHtRZgkbL3BvtNnmg6A5q_bO4v8Zi9Tdfq2Zysh5MiLonG4nbrQSjwAGCp623wJUGLhmTqBmGMq7fRzUz901oXxqFyWpDAWdAaHiye8vOZ3lhnQlDJQ0a11zAcqKcjIi5Q.MRYY3SQNXola7rxlXhBrxfLWnvFT1A1Et7W2cSlP5Eo&dib_tag=se&keywords=RASPBERRY+PI+4&qid=1720372489&s=computers&sprefix=raspberry+pi+4%2Ccomputers%2C125&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1)  
[Tarjeta de sonido USB](https://www.amazon.es/dp/B00DHD8PPE?ref=ppx_yo2ov_dt_b_product_details&th=1)

[Micrófono micro USB](https://www.amazon.es/gp/product/B08BHM9VVW/ref=ox_sc_act_title_1?smid=A19HXCV96LJNAY&psc=1)

[Tarjeta micro SD](https://es.aliexpress.com/item/1005004635543631.html?src=google&src=google&albch=shopping&acnt=439-079-4345&slnk=&plac=&mtctp=&albbt=Google_7_shopping&albagn=888888&isSmbAutoCall=false&needSmbHouyi=false&albcp=18928172568&albag=&trgt=&crea=es1005004635543631&netw=x&device=c&albpg=&albpd=es1005004635543631&gclid=CjwKCAjwjaWoBhAmEiwAXz8DBYf6haE6xSgjybUdS7EWzRFEFk05sSMhARAr1vwOo0HNLKLyF9iLgBoCo6UQAvD_BwE&gclsrc=aw.ds&aff_fcid=3aec91ffbc8a497c9827789aa2d28dc9-1695144512619-01772-UneMJZVf&aff_fsk=UneMJZVf&aff_platform=aaf&sk=UneMJZVf&aff_trace_key=3aec91ffbc8a497c9827789aa2d28dc9-1695144512619-01772-UneMJZVf&terminal_id=30f772f43aff415480e751d9893a0371&afSmartRedirect=y)

[Controlador driver l298n](https://www.amazon.es/OcioDual-Controlador-Motores-Driver-Stepper/dp/B07YNR5KWP/ref=asc_df_B07YNR5KWP/?tag=googshopes-21&linkCode=df0&hvadid=699788246605&hvpos=&hvnetw=g&hvrand=7518927531183041364&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1005492&hvtargid=pla-1875528526707&psc=1&mcid=18ec99e215033d9bab88ec609c0d53ed&gad_source=1)

[Rueda loca](https://www.planetaelectronico.com/rueda-loca-para-robot-diy-p-16998.html)

[Filamento PLA+ 1.75mm](https://www.amazon.es/SUNLU-PLA-3D-1-75mm-dimensional/dp/B07W47D4YZ/ref=sr_1_7?adgrpid=56241830615&dib=eyJ2IjoiMSJ9.g7hg6OyKWiLrTanEhk-fKywiKIyOsiKR45ynx-ZTt6r6zbl7amja3D1CtVccgyp-DLGewO5o4y5UaSDSiLOEP9YVyt5wZ2KMSE7lFJ6X2E_NZoHGe7bz33r0Q_iQH_wCeEBZhHDrooyH46gV14oGGYs3YH_goPcVtE8y-ekbCES2ojM8JPz5Ir-DnOyjfCGWTg6ieLfnH2yzscTeS7EHVxVWRNCIhz8EtJ2be_TVIU9Ql2PIqXyTJH4V9ogW1GjcUrAnALJs7PXWhNziALDGNUguiUv66gBt25NyGV8vDKQ.d5SL9a-RmHAiHKj83hFGjjMEGJok65WnPHJJnA4HVms&dib_tag=se&hvadid=685380943437&hvdev=c&hvlocphy=1005492&hvnetw=g&hvqmt=e&hvrand=8207918468773664201&hvtargid=kwd-320431463035&hydadcr=17380_2261118&keywords=plastico%2Bimpresora%2B3d&qid=1720372270&sr=8-7&th=1)

[Juntas tóricas](https://www.amazon.es/YIXISI-Arandela-Fontaner%C3%ADa-Reparaci%C3%B3n-Autom%C3%A1tica/dp/B0CH84CXLR/ref=sr_1_10?adgrpid=57792598018&dib=eyJ2IjoiMSJ9.5DSZqJ1a_z3CizwbUJMwmjdY7rZ0Spu_hJxaqDQJb7IkznjDk1okA6ZcevX5BdQPQ-kUjz0a0TKgTTuttdQ6fAvBqjDKmptNISyCbpmPFX6TlwE90U6FnFsjU1vpcmBaAYruyv9zBOF8_It_rRgJNV22ttEnbkbZ3OdnYRn9X2YyQN2BAfirFS0VLHkBJrLDVFddqk-cqqKFTCDgz2KjsLAcHJ6DeSy_QPN8-vEGVlGNCuYYVamVGu-hUR9JYf5leGwO0j258cED1Nk_OVzZ8pTmprq9Lnq80EgVtlNkCp0.ryBja1n-VQ7Rd7HtqbNFbKttwKLc8sMZj2oYGdj4ZMI&dib_tag=se&hvadid=275478091626&hvdev=c&hvlocphy=1005492&hvnetw=g&hvqmt=e&hvrand=11040862232827926902&hvtargid=kwd-295574459246&hydadcr=14553_1815238&keywords=juntas+toricas&qid=1720372579&sr=8-10)

En cuanto al entorno de programación, la Raspberry tiene por defecto 
instalado Thonny Python IDE el cual es para proyectos más simples y tiene menos
capacidades que Python 3(IDLE), el cual es más conveniente para este tipo de 
proyectos. Para instalarlo:

```
sudo apt install python3 idle3
``` 

Revisar la [wiki](https://github.com/RoboticsURJC/tfg-vdelatorre/wiki) para más información sobre el proyecto.
