#!/bin/bash

# para executar
# for a in $(ls | head -n 5); do ./lista.sh $a; done

file=$1
file_name=$(basename $file)
dominio=inssgov.onmicrosoft.com

display_name=$(echo "$file_name" | sed 's/.txt$//')

primary_smtp_address=$(head -n 1 "$file")
primary_smtp_address_dominio=$(echo "$primary_smtp_address" | sed "s/@[^\"]*/@$dominio/")

###
#owner=$(sed -n '/^Pode enviar: /,/^Destinatarios: / { s/^Pode enviar: //; /^Destinatarios: /d; p}' "$file")
#owner_dominio=$(if [ -n "$owner" ]; then echo "$owner" | sed "s/@[^\"]*//; s/$/@$dominio/"; fi)

####
owner_list=$(sed -n '/^Pode enviar: /,/^Destinatarios: / { s/^Pode enviar: //; /^Destinatarios: /d; p}' "$file")
#owner=$(echo $owner_list | sed 's/^/"/; s/ /","/g; s/$/"/')
owner=$(echo $owner_list)
owner_dominio=$(echo "$owner" | sed "s/@[^ ]*/@$dominio/g")
#owner_dominio=$(echo "$owner" | sed "s/@inss\.gov\.br/@$dominio/g")

#members_list=$(sed -n '/^Destinatarios: /,$ { s/^Destinatarios: //; p }' "$file")
members_list=$(sed -n '/^Destinatarios: /,/mailForwardingAddress/ { s/^Destinatarios: //; /mailForwardingAddress/d;  p }' "$file")
members=$(echo $members_list | sed 's/^/"/; s/ /","/g; s/$/"/')
#members_dominio=$(echo "$members" | sed "s/@[^\"]*/@$dominio/g")
members_dominio=$(echo "$members" | sed "s/@inss\.gov\.br/@$dominio/g")

## Correto
#echo "New-UnifiedGroup -DisplayName $display_name -PrimarySmtpAddress $primary_smtp_address -Owner $owner -Members $members -AccessType Private"

# Alterando o dominio
#echo "New-UnifiedGroup -DisplayName $display_name -PrimarySmtpAddress $primary_smtp_address -Owner $owner_dominio -Members $members_dominio -AccessType Private"

#comando="New-UnifiedGroup -DisplayName $display_name -PrimarySmtpAddress $primary_smtp_address" 

if [ -n "$owner_dominio" ]
then
  #comando="$comando -Owner $owner_dominio"
  for owner in $(echo "$owner_dominio")
  do
    echo "New-UnifiedGroup -DisplayName $display_name -PrimarySmtpAddress $primary_smtp_address -Owner $owner -AccessType Private"
    echo "Set-UnifiedGroup -Identity $primary_smtp_address_dominio -Language 'pt-BR' -AcceptMessagesOnlyFromSendersOrMembers $owner -RejectMessagesFromSendersOrMembers \$null"
  done
  echo "New-UnifiedGroup -DisplayName $display_name -PrimarySmtpAddress $primary_smtp_address -Owner guiarapido@inss.gov.br -AccessType Private"
  echo "Set-UnifiedGroup -Identity $primary_smtp_address_dominio -Language 'pt-BR' -AcceptMessagesOnlyFromSendersOrMembers  guiarapido@inss.gov.br -RejectMessagesFromSendersOrMembers \$null"
else
  echo "New-UnifiedGroup -DisplayName $display_name -PrimarySmtpAddress $primary_smtp_address -AccessType Private"
  echo "Set-UnifiedGroup -Identity $primary_smtp_address_dominio -Language 'pt-BR' -RejectMessagesFromSendersOrMembers \$null"
fi

#if [ "$members_dominio" != '""' ]
#then
#  comando="$comando -Members $members_dominio"
#fi

#comando="$comando -AccessType Private"

#echo "$comando"

### Parte 2
for membro in $(echo "$members_dominio" | sed 's/,/ /g')
do
    #echo "Set-UnifiedGroup -Identity $primary_smtp_address_dominio -Language 'pt-BR' -AcceptMessagesOnlyFromSendersOrMembers $membro -RejectMessagesFromSendersOrMembers \$null"
    echo "Add-UnifiedGroupLinks –Identity \"$primary_smtp_address_dominio\" –LinkType "Members" –Links $membro"
done

owner_pt2=$(sed -n '/^Pode enviar: /,/^Destinatarios: / { s/^Pode enviar: //; /^Destinatarios: /d; p}' "$file")
owner_dominio_pt2=$(if [ -n "$owner_pt2" ]; then echo "$owner_pt2" | sed "s/@[^\"]*//; s/$/@$dominio/" | sort -u; fi)
owner_dominio_pt2=$(echo $owner_dominio_pt2 | sed 's/^/"/; s/ /","/g; s/$/"/' )

#echo "Set-UnifiedGroup -Identity $primary_smtp_address_dominio -Language 'pt-BR' -AcceptMessagesOnlyFromSendersOrMembers $owner_dominio_pt2 -RejectMessagesFromSendersOrMembers \$null"

##'if [ -n "$owner_dominio" ]
##'then
##'  #comando="$comando -Owner $owner_dominio"
##'  for owner in $(echo "$owner_dominio")
##'  do
##'    echo "Set-UnifiedGroup -Identity $primary_smtp_address_dominio -Language 'pt-BR' -AcceptMessagesOnlyFromSendersOrMembers $owner_dominio -RejectMessagesFromSendersOrMembers \$null"
##'  done
##'    echo "Set-UnifiedGroup -Identity $primary_smtp_address_dominio -Language 'pt-BR' -AcceptMessagesOnlyFromSendersOrMembers guiarapido@inss.gov.br -RejectMessagesFromSendersOrMembers \$null"
##'else
##'  echo "Set-UnifiedGroup -Identity $primary_smtp_address_dominio -Language 'pt-BR' -RejectMessagesFromSendersOrMembers \$null"
##'fi
