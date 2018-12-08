library(arules)
library(dplyr)
library(arulesViz)


usjh=read.csv('USJH.csv')
head(usjh)

usjh=usjh %>%
  mutate(vendor_category=paste(usjh$vendor, usjh$category, sep=':'))

write.csv(usjh, file = "USJH_rules.csv")

#create proper format for association rules
usjh_ar=as(split(usjh$category, usjh$name), "transactions")
usjh_ar1=as(split(usjh$lineitem_name, usjh$name), "transactions")
usjh_ar2=as(split(usjh$vendor, usjh$name), "transactions")
usjh_ar3=as(split(usjh$vendor_category, usjh$name), "transactions")



#The default behavior is to mine rules with minimum support of 0.1,
#minimum confidence of 0.8, maximum of 10 items (maxlen), 
#and a maximal time for subset checking of 5 seconds (maxtime).
rules=apriori (usjh_ar, parameter = list(supp = 0.02, conf = 0.2))
rules1=apriori (usjh_ar1, parameter = list(supp = 0.002, conf = 0.2))
rules2=apriori (usjh_ar2, parameter = list(supp = 0.02, conf = 0.2))
rules3=apriori (usjh_ar3, parameter = list(supp = 0.02, conf = 0.2))

#inspect rules
arules::inspect(rules)
#convert rules to data frame
ruledf = data.frame(lhs = labels(lhs(rules3)),rhs = labels(rhs(rules3)), rules3@quality)
head(ruledf)

write.csv(ruledf, file = "vendor_cate_rules.csv")

inspect(head(rules, n=20, by='lift'))
inspect(head(rules1, n=20, by='lift'))
inspect(head(rules2, n=20, by='lift'))
inspect(head(rules3, n=20, by='support'))

head(quality(rules))
plot(rules)

plot(rules, measure = c("support", "lift"), shading = "confidence")

plot(rules, method = "two-key plot")

#category/name
summary(usjh_ar)

#most frequent items:
# necklace     earring    bracelet     apparel accessories     (Other) 
#2658        2474        1573         864         537         923 

537/9000

subrules <- head(rules, n = 10, by = "lift")
subrules
plot(subrules, method='matrix', measure = 'lift')
plot(subrules, method = "graph")
plot(rules, method = "grouped")

#lineitem name/name
summary(usjh_ar1)

#most frequent items:
#urban geometric metal hoop earrings - gold      lightweight urban brass earrings - gold 
#108                                           99 
#lightweight urban brass earrings - silver urban geometric metal hoop earrings - silver 
#89                                           86 
#geometric metal hoop earrings - gold                                      (Other) 
#74                                        78765 

subrules1 <- head(rules1, n = 10, by = "lift")
subrules1
plot(subrules1, method='matrix', measure = 'lift')
plot(subrules1, method = "graph")
plot(rules1, method = "grouped", gp_labels = gpar(cex=0.4))

#vendor/name
summary(usjh_ar2)

#most frequent items:
#usjewelryhouse          cloie        romance        dorothy     it's sense        (Other) 
#2629           1128           1128           1025           1002          14045 

subrules2 <- head(rules2, n = 10, by = "lift")
subrules2
plot(subrules2, method='matrix', measure = 'lift')
plot(subrules2, method = "graph")
plot(rules2, method = "grouped",gp_labels = gpar(cex=0.6))

#vendor_category/name
summary(usjh_ar3)

#most frequent items:
#  usjewelryhouse:necklace  usjewelryhouse:earring usjewelryhouse:bracelet           cloie:earring 
#1790                    1295                     985                     820 
#it's sense:earring                 (Other) 
#796                   21236 

subrules3 <- head(rules3, n = 10, by = "lift")
subrules3
plot(subrules3, method='matrix', measure = 'lift')
plot(subrules3, method = "graph")
plot(rules3, method = "grouped",gp_labels = gpar(cex=0.5, gp_main='Vender:Category'))

#========================================================================
uno_sale=read.csv('UNO_Sale_vs_RCVD_modified.csv')


uno_des=uno_sale %>%
  filter(!is.na(description))
uno_des$description=trimws(gsub("[^A-Za-z ]","",uno_des$description))

uno_des$description

uno_des_ar=as(split(uno_des$description, uno_des$cust), "transactions") #it removes duplicated item automatically


Rules=apriori (uno_des_ar, parameter = list(supp = 0.1, conf = 0.2))


#description/cust
summary(uno_des_ar)
#most frequent items:
#  TASSEL METAL HOOK ER                      TASSEL NK                  METAL DROP ER 
#116                            111                            110 
#Y SHAPED CHAIN TASSEL  LONG NK               METAL LAYERED NK                        (Other) 
#105                             91                          27659
subRules <- head(Rules, n = 20, by = "lift")
subRules
plot(subRules, method='matrix', measure = 'lift')
plot(subRules, method = "graph")
plot(subRules, method = "grouped", gp_labels = gpar(cex=0.4))
  