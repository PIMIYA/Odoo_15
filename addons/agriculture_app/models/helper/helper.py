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
                partner.zip, partner.state_id.name, partner.street, partner.street2)
        else:
            return "{0}{1}{2}{3}{4}".format(
                partner.zip, partner.state_id.name, partner.city, partner.street,
                partner.street2)
    else:
        if partner.state_id.name == partner.city:
            return "{0}{1}{2}".format(
                partner.zip, partner.state_id.name, partner.street)
        else:
            return "{0}{1}{2}{3}".format(
                partner.zip, partner.state_id.name, partner.city, partner.street)
