#!/usr/bin/env bash
sed -i 's#<adj> thai </adj>#thai#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> recommend </adj>#recommend#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> recommended </adj>#recommended#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> i </adj>#i#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> single </adj>#single#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> table </adj>#table#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> te </adj>#te#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> thursday </adj>#thursday#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> om </adj>#om#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> much </adj>#much#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> entire </adj>#entire#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> nyc </adj>#nyc#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> dole </adj>#dole#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> added </adj>#added#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> crumble </adj>#crumble#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> such </adj>#such#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> loved </adj>#loved#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> open-concept </adj>#open-concept#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> drinks </adj>#drinks#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> bolognese </adj>#bolognese#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> pasta </adj>#pasta#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> wine </adj>#wine#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> san </adj>#san#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> sum </adj>#sum#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> willow </adj>#willow#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> local </adj>#local#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> sustainable </adj>#sustainable#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> olive </adj>#olive#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> tomato-coconut </adj>#tomato-coconut#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> website </adj>#website#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> current </adj>#current#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> birthday </adj>#birthday#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> tapa </adj>#tapa#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> crepe </adj>#crepe#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> pet </adj>#pet#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> only </adj>#only#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> papaya </adj>#papaya#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> citrus </adj>#citrus#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> due </adj>#due#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> kiss </adj>#kiss#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> several </adj>#several#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> lemon </adj>#lemon#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> possible </adj>#possible#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> fish </adj>#fish#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> other </adj>#other#g' ../Data/Dev_Set/*.txt

# Tag the adjectives if not tagged
sed -i 's#oily#<adj> oily </adj>#g' ../Data/Dev_Set/*.txt
sed -i 's#greasy#<adj> greasy </adj>#g' ../Data/Dev_Set/*.txt
sed -i 's#salty#<adj> salty </adj>#g' ../Data/Dev_Set/*.txt


# Incorrectly formed tags
sed -i 's#<<adj> adj </adj>>#<adj>#g' ../Data/Dev_Set/*.txt
sed -i 's#</<adj> adj </adj>>#</adj>#g' ../Data/Dev_Set/*.txt
sed -i 's#<adj> <adj>#<adj>#g' ../Data/Dev_Set/*.txt
sed -i 's#</adj> </adj>#</adj>#g' ../Data/Dev_Set/*.txt