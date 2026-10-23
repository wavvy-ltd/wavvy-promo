#!/bin/bash
# Inject realistic M-Pesa SMS into the running emulator so the parser, tagging,
# budgets and notifications run on real messages. Usage: scripts/seed_sms.sh [delay_s]
set -e
DELAY=${1:-4}
send() {
  adb emu sms send MPESA "$1" >/dev/null
  echo "sent: ${1:0:60}..."
  sleep "$DELAY"
}

send "TJ1A2B3C4D Confirmed.You have received Ksh45,000.00 from SISITECH LTD 254722000111 on 1/10/26 at 9:02 AM New M-PESA balance is Ksh52,310.50. Separate personal and business funds through Pochi la Biashara on *334#."
send "TJ1F8K2L9M Confirmed. Ksh12,000.00 sent to JANE WANJIRU 0712345678 on 1/10/26 at 6:30 PM. New M-PESA balance is Ksh40,310.50. Transaction cost, Ksh55.00. Amount you can transact within the day is 487,945.00."
send "TJ2C4D5E6F Confirmed. Ksh2,450.00 paid to NAIVAS SUPERMARKET. on 2/10/26 at 1:15 PM.New M-PESA balance is Ksh37,860.50. Transaction cost, Ksh0.00. Amount you can transact within the day is 497,550.00."
send "TJ2G7H8I9J Confirmed. Ksh650.00 paid to JAVA HOUSE KIMATHI. on 3/10/26 at 8:40 AM.New M-PESA balance is Ksh37,210.50. Transaction cost, Ksh0.00. Amount you can transact within the day is 499,350.00."
send "TJ3K1L2M3N Confirmed. Ksh3,200.00 sent to KENYA POWER for account 12345678 on 4/10/26 at 7:05 PM New M-PESA balance is Ksh34,010.50. Transaction cost, Ksh0.00. Amount you can transact within the day is 496,800.00."
send "TJ4P5Q6R7S Confirmed. Ksh1,500.00 sent to ZUKU for account 9988776 on 5/10/26 at 10:12 AM New M-PESA balance is Ksh32,510.50. Transaction cost, Ksh0.00."
send "TJ5T8U9V0W Confirmed. Ksh500.00 of airtime purchased for 0722000111 on 6/10/26 at 3:33 PM. New M-PESA balance is Ksh32,010.50. Transaction cost, Ksh0.00."
send "TJ6X1Y2Z3A Confirmed. Ksh1,200.00 paid to SIMBISA ONLINE. on 7/10/26 at 1:02 PM.New M-PESA balance is Ksh30,810.50. Transaction cost, Ksh0.00."
send "TJ7B4C5D6E Confirmed. Ksh350.00 paid to UBER KENYA. on 8/10/26 at 9:17 AM.New M-PESA balance is Ksh30,460.50. Transaction cost, Ksh0.00."
send "TJ8F7G8H9I Confirmed. Ksh850.00 paid to CHICKEN INN. on 9/10/26 at 8:05 PM.New M-PESA balance is Ksh29,610.50. Transaction cost, Ksh0.00."
send "TJ9J0K1L2M Confirmed.on 10/10/26 at 11:20 AMWithdraw Ksh5,000.00 from 123456 - MOI AVENUE AGENT New M-PESA balance is Ksh24,610.50. Transaction cost, Ksh105.00."
send "TK1N3O4P5Q Confirmed. Ksh2,000.00 sent to SAFARICOM POSTPAID for account 0722000111 on 11/10/26 at 6:00 PM New M-PESA balance is Ksh22,610.50. Transaction cost, Ksh0.00."
send "TK2R6S7T8U Confirmed. Ksh1,800.00 paid to QUICKMART. on 12/10/26 at 5:48 PM.New M-PESA balance is Ksh20,810.50. Transaction cost, Ksh0.00."
send "TK3V9W0X1Y Confirmed. Ksh700.00 paid to ARTCAFFE. on 13/10/26 at 12:30 PM.New M-PESA balance is Ksh20,110.50. Transaction cost, Ksh0.00."
send "TK4Z2A3B4C Confirmed. Ksh4,000.00 sent to MAMA MBOGA 0733111222 on 14/10/26 at 7:45 PM. New M-PESA balance is Ksh16,110.50. Transaction cost, Ksh29.00."
send "TK5D5E6F7G Confirmed.You have received Ksh6,500.00 from PETER OTIENO 254711222333 on 15/10/26 at 2:10 PM New M-PESA balance is Ksh22,610.50."
send "TK6H8I9J0K Confirmed. Ksh950.00 paid to NETFLIX.COM. on 16/10/26 at 9:00 AM.New M-PESA balance is Ksh21,660.50. Transaction cost, Ksh0.00."
send "TK7L1M2N3O Confirmed. Ksh420.00 paid to LITTLE CAB. on 17/10/26 at 8:22 AM.New M-PESA balance is Ksh21,240.50. Transaction cost, Ksh0.00."
send "TK8P4Q5R6S Confirmed. Ksh1,350.00 paid to CARREFOUR TWO RIVERS. on 18/10/26 at 4:05 PM.New M-PESA balance is Ksh19,890.50. Transaction cost, Ksh0.00."
send "TK9T7U8V9W Confirmed. Ksh600.00 paid to KFC WESTLANDS. on 19/10/26 at 7:30 PM.New M-PESA balance is Ksh19,290.50. Transaction cost, Ksh0.00."
send "TL1X0Y1Z2A Confirmed. Ksh2,500.00 sent to NAIROBI WATER for account 556677 on 20/10/26 at 10:40 AM New M-PESA balance is Ksh16,790.50. Transaction cost, Ksh0.00."
send "TL2B3C4D5E Confirmed. Ksh780.00 paid to JAVA HOUSE KIMATHI. on 21/10/26 at 1:12 PM.New M-PESA balance is Ksh16,010.50. Transaction cost, Ksh0.00."
send "TL3F6G7H8I Confirmed. Ksh1,100.00 paid to TOTAL ENERGIES NGONG RD. on 22/10/26 at 6:50 PM.New M-PESA balance is Ksh14,910.50. Transaction cost, Ksh0.00."
send "TL4J9K0L1M Confirmed. Ksh540.00 paid to CHICKEN INN. on 23/10/26 at 12:05 PM.New M-PESA balance is Ksh14,370.50. Transaction cost, Ksh0.00."
echo "done"
