def get_phone_info(partner: object):
    if partner.mobile:
        if partner.mobile.startswith('+886'):
            return partner.mobile.replace('+886', '0').replace(" ", "")
        else:
            return partner.mobile.replace(" ", "")
    elif partner.phone:
        if partner.phone.startswith('+886'):
            return partner.phone.replace('+886', '0').replace(" ", "")
        else:
            return partner.phone.replace(" ", "")
    else:
        return None


def get_address_info(partner: object):
    if partner.street2:
        if partner.state_id.name == partner.city:
            return "{0}{1}{2}{3}".format(
                str(partner.zip or ''),
                str(partner.state_id.name or ''),
                str(partner.street or ''),
                str(partner.street2 or ''))
        else:
            return "{0}{1}{2}{3}{4}".format(
                str(partner.zip or ''),
                str(partner.state_id.name or ''),
                str(partner.city or ''),
                str(partner.street or ''),
                str(partner.street2 or ''))
    else:
        if partner.state_id.name == partner.city:
            return "{0}{1}{2}".format(
                str(partner.zip or ''),
                str(partner.state_id.name or ''),
                str(partner.street or ''))
        else:
            return "{0}{1}{2}{3}".format(
                str(partner.zip or ''),
                str(partner.state_id.name or ''),
                str(partner.city or ''),
                str(partner.street or ''))


def get_company_phone(company: object):
    return get_phone_info(company)


def get_company_address(company: object):
    if company.state_id.name == company.city:
        return "{0}{1}{2}".format(
            str(company.zip or ''),
            str(company.city or ''),
            str(company.street or ''))
    else:
        return "{0}{1}{2}{3}".format(
            str(company.zip or ''),
            str(company.state_id.name or ''),
            str(company.city or ''),
            str(company.street or ''))
