# Focused re-run of the BMA heterogeneity path (Table 4) and the implied-context
# effects (Table 5), reproduced from the authors' incentives.R (sections 3-4),
# reading the Stata-made intermediate auxiliaries/incentives_4R.csv.
# Adds the explicit "Laboratory + loss framing" combined cell (finding F-078).
suppressPackageStartupMessages(library(BMS))
set.seed(2025)  # for a reproducible re-run (the authors set no seed; MCMC PIPs are stable at these counts)

AUX <- "auxiliaries"; RES <- "results"
if(!dir.exists(RES)) dir.create(RES)

incentives <- read.csv(file.path(AUX, "incentives_4R.csv"), header = TRUE)
incentives <- na.omit(incentives)
colnames(incentives) <- c("Study ID","PCC","Standard error","Preferred estimate","SE * Control","Effect: grades","Effect: charity","Effect: game","Effect: work","Effect: positive","Task: appealing","Task: unappealing","Task: cognitive","Task: manual","Performance: quantitative","Performance: qualitative","Reward size","Positive framing","Negative framing","All subjects paid","Individual reward","Group reward","Control: no incentive","Motivation: altruism","Motivation: reciprocity","Motivation: fairness","Motivation: money only","Laboratory experiment","Field experiment","Crowding-out theory","Subjects: students","Subjects: employees","Subjects: general","Gender: males","Gender: females","Subjects' age","Data year","Developed country","Method: OLS","Method: logit","Method: probit","Method: tobit","Method: fixed-effects","Method: random-effects","Method: DID","Method: Other","Cross-section","Panel","Impact factor","Citations")
data_new <- c("PCC","Standard error","Preferred estimate","Effect: grades","Effect: charity","Effect: game","Effect: positive","Task: appealing","Task: cognitive","Performance: quantitative","Reward size","Positive framing","All subjects paid","Individual reward","Control: no incentive","Motivation: altruism","Motivation: reciprocity","Motivation: fairness","Laboratory experiment","Crowding-out theory","Subjects: students","Subjects: employees","Gender: males","Subjects' age","Data year","Developed country","Method: OLS","Method: logit","Method: probit","Method: tobit","Method: fixed-effects","Method: random-effects","Method: DID","Cross-section","Impact factor","Citations")
data_df <- incentives[, data_new, drop = FALSE]
cat("data_df dim:", dim(data_df)[1], "x", dim(data_df)[2], "\n")

# --- Table 4: BMA (UIP g-prior, dilution model prior) ---
incentives1 <- bms(data_df, burn=1e5, iter=3e5, g="UIP", mprior="dilut", nmodel=50000, mcmc="bd", user.int=FALSE)
co <- coef(incentives1, order.by.pip=TRUE, exact=TRUE, include.constant=TRUE)
write.csv(co, file.path(RES, "rerun_bma_dilut_coef.csv"))
cat("\n=== Table 4 (BMA dilut) PIP / PostMean (top) ===\n"); print(round(co,4))

# --- Table B12 robustness: BRIC g-prior, random model prior ---
incentives2 <- bms(data_df, burn=1e5, iter=3e5, g="BRIC", mprior="random", nmodel=50000, mcmc="bd", user.int=FALSE)
co2 <- coef(incentives2, order.by.pip=TRUE, exact=TRUE, include.constant=TRUE)
write.csv(co2, file.path(RES, "rerun_bma_bric_coef.csv"))
cat("\n=== Table B12 (BMA BRIC/random) PIP for Lab + framing ===\n")
print(round(co2[rownames(co2) %in% c("Laboratory experiment","Positive framing"),],4))

# --- Table 5: implied effects for different contexts (best-practice linear combination) ---
bma_coefs <- coef(incentives1, include.constant=TRUE, exact=TRUE)
post_means <- bma_coefs[, "Post Mean"]
input_vars <- data_df[, -1]
sample_means <- colMeans(input_vars, na.rm=TRUE)
calc_lincom <- function(scenario_name, overrides=list()){
  cur <- sample_means
  if("Standard error" %in% names(cur)) cur["Standard error"] <- 0
  if("Preferred estimate" %in% names(cur)) cur["Preferred estimate"] <- 1
  for(v in names(overrides)) if(v %in% names(cur)) cur[v] <- overrides[[v]]
  vim <- setdiff(names(post_means), c("(Intercept)","Intercept"))
  intc <- post_means[which(names(post_means) %in% c("(Intercept)","Intercept"))]; if(length(intc)==0) intc <- 0
  data.frame(Scenario=scenario_name, Mean_Effect=as.numeric(intc + sum(post_means[vim]*cur[vim], na.rm=TRUE)))
}
rl <- list()
rl[[1]] <- calc_lincom("Mean best practice")
rl[[2]] <- calc_lincom("Laboratory experiment", list("Laboratory experiment"=1))
rl[[3]] <- calc_lincom("Field experiment", list("Laboratory experiment"=0))
rl[[4]] <- calc_lincom("Positive framing", list("Positive framing"=1))
rl[[5]] <- calc_lincom("Negative (loss) framing", list("Positive framing"=0))
# F-078 fix: the explicit combined lab + loss-framing cell the paper reports in prose but never tabulates
rl[[6]] <- calc_lincom("Laboratory + loss framing", list("Laboratory experiment"=1, "Positive framing"=0))
final_table <- do.call(rbind, rl); row.names(final_table) <- NULL
write.csv(final_table, file.path(RES, "rerun_table5_implied.csv"), row.names=FALSE)
cat("\n=== Table 5 (implied effects) regenerated ===\n"); print(round(final_table[,2,drop=FALSE],4)->junk); print(final_table)

# machine-readable key numbers for the provenance/repro report
lab <- final_table$Mean_Effect[final_table$Scenario=="Laboratory experiment"]
labloss <- final_table$Mean_Effect[final_table$Scenario=="Laboratory + loss framing"]
pip_lab <- co[ "Laboratory experiment","PIP"]
pip_posframing <- co[ "Positive framing","PIP"]
pip_posframing_bric <- co2[ "Positive framing","PIP"]
key <- list(n_obs=nrow(data_df), n_reg=ncol(data_df)-1,
            pip_lab=round(pip_lab,4), pip_posframing_dilut=round(pip_posframing,4),
            pip_posframing_bric=round(pip_posframing_bric,4),
            implied_lab=round(lab,4), implied_lab_loss=round(labloss,4))
writeLines(jsonlite_like <- paste0("{",paste(sprintf('"%s": %s', names(key), unlist(key)), collapse=", "),"}"),
           file.path(RES,"rerun_keynumbers.json"))
cat("\n=== KEY NUMBERS ===\n"); cat(jsonlite_like, "\n")
cat("\nBMA_RERUN_DONE\n")
