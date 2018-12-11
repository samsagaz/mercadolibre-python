import requests
import time

from mercadolibre import exceptions
from mercadolibre.decorators import valid_token
from urllib.parse import urlencode


class Client(object):
    BASE_URL = 'https://api.mercadolibre.com'

    auth_urls = {
        'MLA': "https://auth.mercadolibre.com.ar",  # Argentina
        'MLB': "https://auth.mercadolibre.com.br",  # Brasil
        'MCO': "https://auth.mercadolibre.com.co",  # Colombia
        'MCR': "https://auth.mercadolibre.com.cr",  # Costa Rica
        'MEC': "https://auth.mercadolibre.com.ec",  # Ecuador
        'MLC': "https://auth.mercadolibre.cl",  # Chile
        'MLM': "https://auth.mercadolibre.com.mx",  # Mexico
        'MLU': "https://auth.mercadolibre.com.uy",  # Uruguay
        'MLV': "https://auth.mercadolibre.com.ve",  # Venezuela
        'MPA': "https://auth.mercadolibre.com.pa",  # Panama
        'MPE': "https://auth.mercadolibre.com.pe",  # Peru
        'MPT': "https://auth.mercadolibre.com.pt",  # Prtugal
        'MRD': "https://auth.mercadolibre.com.do"  # Dominicana
    }

    def __init__(self, client_id, client_secret, site='MCO'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self._refresh_token = None
        self.user_id = None
        self.expires_in = None
        self.expires_at = None
        try:
            self.auth_url = self.auth_urls[site]
        except KeyError as e:
            raise exceptions.InvalidSite()

    def authorization_url(self, redirect_uri):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri
        }
        url = self.auth_url + '/authorization?' + urlencode(params)
        return url

    def exchange_code(self, redirect_uri, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        return self._token(self._post('/oauth/token', params=params))

    def refresh_token(self):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token,
        }
        return self._token(self._post('/oauth/token', params=params))

    def set_token(self, token):
        if isinstance(token, dict):
            self.access_token = token.get('access_token', None)
            self._refresh_token = token.get('refresh_token', None)
            self.user_id = token.get('user_id', None)
            self.expires_in = token.get('expires_in', None)
            self.expires_at = token.get('expires_at', None)
        else:
            self.access_token = token

    @property
    def is_valid_token(self):
        if self.expires_at:
            return self.expires_at > time.time()
        else:
            return None

    @valid_token
    def me(self):
        """Returns account information about the authenticated user.

        Returns:
            A dict.
        """
        return self._get('/users/me')

    @valid_token
    def get_user(self, user_id):
        """User account information.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}'.format(user_id))

    @valid_token
    def update_user(self, user_id, identification_type, identification_number, address,
                    state, city, zip_code, phone, phone_area_code, phone_number, phone_extension,
                    first_name, last_name, company, company_corporate_name, company_brand_name,
                    mercadoenvios):
        """Update User account.

        Args:
            user_id:
            identification_type:
            identification_number:
            address:
            state:
            city:
            zip_code:
            phone:
                area_code:
                number:
                extension:
            first_name:
            last_name:
            company:
                corporate_name:
                brand_name:
            mercadoenvios:

        Returns:
            A dict.
        """
       data = {
            'user_id': user_id,
            'identification_type': identrification_type,
            'identification_number': identification_number,
            'address': address,
            'state': state,
            'city': city,
            'zip_code': zip_code,
            'phone': phone,
            'area_code': phone.area_code,
            'number': phone.number,
            'extension': phone.extension,
            'first_name': first_name,
            'last_name': last_name,
            'company': company,
            'corporate_name': company.corporate_name,
            'brand_name': company.brand_name,
            'mercadoenvios': mercadoenvios,
        }
        data.update(kwargs)
        return self._post('/users', json=data)


    @valid_token
    def get_user_address(self, user_id):
        """Returns addresses registered by the user.

        Args:
            user_id:

        Returns:
            A list.
        """
        return self._get('/users/{}/addresses'.format(user_id))

    @valid_token
    def get_user_accepted_payment_methods(self, user_id):
        """Returns payment methods accepted by a seller to collect its operations.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}/accepted_payment_methods'.format(user_id))

    @valid_token
    def get_application(self, application_id):
        """Returns information about the application.

        Args:
            application_id:

        Returns:
            A dict.
        """
        return self._get('/applications/{}'.format(application_id))

    @valid_token
    def get_user_brands(self, user_id):
        """This resource retrieves brands associated to an user_id. The official_store_id attribute identifies a store.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}/brands'.format(user_id))

    @valid_token
    def get_user_classifields_promotion_packs(self, user_id):
        """Manage user promotion packs.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}/classifieds_promotion_packs'.format(user_id))

    def create_user_classifields_promotion_packs(self):
        raise NotImplementedError

    @valid_token
    def get_project(self, project_id):
        """Manage projects.

        Returns:
            A dict.
        """
        return self._get('/projects/{}'.format(project_id))

    def create_project(self):
        raise NotImplementedError

    def update_project(self):
        raise NotImplementedError

    def delete_project(self):
        raise NotImplementedError

    @valid_token
    def get_available_listing_types(self, user_id):
        """Manage user available listing types.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}/available_listing_types'.format(user_id))

    @valid_token
    def get_available_listing_types_by_category(self, user_id, category_id):
        """Manage user available listing types by category.

        Args:
            user_id:
            category_id:

        Returns:
            A dict.
        """
        return self._get('/users/{}/available_listing_types?category_id={}'.format(user_id, category_id))

    @valid_token
    def revoke_application_permissions(self, user_id):
        """Revoke user authorization from app.

        Args:
            user_id:

        Returns:
            A dict.
        """
        return self._delete('/users/{}/applications/{}'.format(user_id, self.client_id))

    @valid_token
    def get_my_feeds(self):
        """Notifications history.

        Returns:
            A dict.
        """
        params = {
            'app_id': self.client_id
        }
        return self._get('/myfeeds', params=params)

    @valid_token
    def get_sites(self):
        """Retrieves information about the sites where MercadoLibre runs.

        Returns:
            A list.
        """
        return self._get('/sites')

    @valid_token
    def get_listing_types(self, site_id):
        """Returns information about listing types.

        Args:
            site_id:

        Returns:
            A dict.
        """
        return self._get('/sites/{}/listing_types'.format(site_id))

    @valid_token
    def get_listing_exposures(self, site_id):
        """Returns different exposure levels associated with all listing types in MercadoLibre.

        Args:
            site_id:

        Returns:
            A dict.
        """
        return self._get('/sites/{}/listing_exposures'.format(site_id))

    @valid_token
    def get_categories(self, site_id):
        """	Returns available categories in the site.

        Args:
            site_id:

        Returns:
            A list.
        """
        return self._get('/sites/{}/categories'.format(site_id))

    @valid_token
    def get_category(self, category_id):
        """Returns information about a category.

        Args:
            category_id:

        Returns:
            A dict.
        """
        return self._get('/categories/{}'.format(category_id))

    @valid_token
    def get_category_attributes(self, category_id):
        """Displays attributes and rules over them in order to describe the items that are stored in each category.

        Args:
            category_id:

        Returns:
            A dict.
        """
        return self._get('/categories/{}/attributes'.format(category_id))

    @valid_token
    def get_category_predictor(self, site_id, title):
        """Retrieves the most accurate category to list your item basing on it's title.

        Args:
            site_id:
            title:

        Returns:
            A dict.
        """
        return self._get('/sites/{}/category_predictor/predict?title={}'.format(site_id, title))


# /categories/{Category_id}/classifieds_promotion_packs	Retrieves classified promotion packs by category.
# /sites/{site_id}/listing_types/{listing_type_id}	Retrieves the configuration for a specific listing type.




# /classified_locations/countries *	Returns countries information.
# /classified_locations/countries/{Country_id} *	Returns country information by country_id.
# /classified_locations/states/{State_id} *	Returns state information.
# /classified_locations/cities/{City_id} *	Returns city information.





    @valid_token
    def get_countries(self):
        """Returns countries information.

        Returns:
            A list.
        """
        return self._get('/countries')

    @valid_token
    def get_country(self, country_id):
        """Returns country information by country_id.

        Returns:
            A dict.
        """
        return self._get('/countries/{}'.format(country_id))

    @valid_token
    def get_state(self, state_id):
        """	Returns state information.

        Args:
            state_id:

        Returns:
            A dict.
        """
        return self._get('/states/{}'.format(state_id))

    @valid_token
    def get_city(self, city_id):
        """Returns city information.

        Args:
            city_id:

        Returns:
            A dict.
        """
        return self._get('/cities/{}'.format(city_id))

# /countries/{Country_id}/zip_codes/{Zip_code}	Retrieves data for the location of the zip code entered.
# /country/{Country_id}/zip_codes/search_between?zip_code_from={zip_code_from}&zip_code_to={zip_code_to}	Retrieve all zip codes for a country_id between two given zip codes.



    @valid_token
    def get_currencies(self):
        """	Returns information about all available currencies in MercadoLibre.

        Returns:
            A list.
        """
        return self._get('/currencies')

    @valid_token
    def get_currency(self, currency_id):
        """Returns information about available currencies in MercadoLibre by currency_id.

        Args:
            currency_id:

        Returns:
            A dict.
        """
        return self._get('/currencies/{}'.format(currency_id))

# /currency_conversions/search?from={Currency_id}&to={Currency_id}	Retrieves the conversion ratio between currencies that MercadoLibre uses in calculations.

    @valid_token
    def list_item(self, title, condition, category_id, price, currency_id, available_quantity, buying_mode,
                  listing_type_id, warranty, description=None, video_id=None, pictures=None, **kwargs):
        """

        Args:
            title:
            condition:
            category_id:
            price:
            currency_id:
            available_quantity:
            buying_mode:
            listing_type_id:
            warranty:
            description:
            video_id:
            pictures:
            **kwargs:

        Returns:
            A dict.
        """
        data = {
            'title': title,
            'condition': condition,
            'category_id': category_id,
            'price': price,
            'currency_id': currency_id,
            'available_quantity': available_quantity,
            'buying_mode': buying_mode,
            'listing_type_id': listing_type_id,
            'warranty': warranty,
        }
        if description:
            data['description'] = description
        if video_id:
            data['video_id'] = video_id
        if pictures:
            if isinstance(pictures, str):
                pictures = [{'source': pictures}]
            elif isinstance(pictures, list):
                pictures = [{'source': p} for p in pictures]
            else:
                raise exceptions.InvalidPictureParameter()
            data['pictures'] = pictures
        data.update(kwargs)
        return self._post('/items', json=data)












# /items/{Item_id}	Allows managing listings
# /items/validate	Validate the JSON before posting an item.
# /items/{Item_id}/available_upgrades	Returns available listing types to upgrade an item exposure.
# /items/{Item_id}/relist	Allows to relist an item.
# pictures/{picture_id}	Manage item pictures.
# /items/{Item_id}/description	Manage description for an item.
# /sites/{Site_id}/search?q=ipod&access_token=$ACCESS_TOKEN	Retrieves items from a search query.
# /sites/{Site_id}/searchUrl?q=ipod&access_token=$ACCESS_TOKEN	Search for any item in MercadoLibre. It will return an array of items url that match the search criteria.
# /sites/MLA/search?category={Category_id}&official_store_id=all&access_token=$ACCESS_TOKEN	Search for all items listed by Official Stores for a given category.
# /sites/{Site_id}/hot_items/search?limit=5&category={Category_id}&access_token=$ACCESS_TOKEN	Retrieves an array of hot items from a specified category by parameter. Works only with the first level of categories.
# /sites/{Site_id}/featured_items/HP-{Category_Id}	Retrieves an array of featured items. The featured items are items that have a special exposure at home page or categories page. You can use only HP for products of home or HP-{categId} for featured by category. Only works with first level of categories.
# /sites/{Site_id}/trends/search?category={Category_id}&access_token=$ACCESS_TOKEN	Retrieve an array of the trends items from the category specified by parameter.
# /sites/{Site_id}/search?seller_id={Seller_id}&category={Category_id}&access_token=$ACCESS_TOKEN	Search items by seller_id for a category.
# /users/{Cust_id}/items/search?access_token=$ACCESS_TOKEN	Retrieves user's items.
# /items/{Item_id}/variations	Manage item's variations.
# /items/{Item_id}/variations/{Variation_id}	Manage variations.
# /users/{Cust_id}/items/search?sku={seller_custom_field}&status=active&access_token=$ACCESS_TOKEN	Search item by SKU. Filter item by status.
# /users/{Cust_id}/items/search?tags=price_review&access_token={access_token}	View items with price_review
# /users/{Cust_id}/items/search?tags=incomplete_technical_specs&access_token={access_token}	It allows reviewing publications that are losing exposure due to not having the complete technical sheets.





# /questions/search?item={Item_id}&access_token=$ACCESS_TOKEN	Search any question made to user's items.
# /questions/{Item_id}	Ask questions on other user's items.
# /answers	Answer questions made on your items.
# /questions/{Question_id}	Retrieves information for an specific question id.
# /users/{Seller_id}/questions_blacklist/$Buyerid?access_token=$ACCESS_TOKEN	Manage questions blacklist.
# /my/received_questions/search	Received questions by user.





# /orders/search?seller={Seller_id}&access_token=$ACCESS_TOKEN	Search the orders from a selle
# /orders/search?seller={Seller_id}&q={Order_id}&access_token=$ACCESS_TOKEN	Search one order from a seller
# /orders/search?buyer={Buyer_id}&access_token=$ACCESS_TOKEN	Search the orders from a buyer
# /payments/{Payment_id}?access_token=$ACCESS_TOKEN	Returns data for a payment, according to the profile of the sender of the payment.
# /sites/{Site_id}/payment_methods	Returns the payment methods provided by MercadoPago.
# sites/$Site_id/payment_methods/$id	Returns the detail of the specific payment method.
# /orders/{Order_id}/feedback?access_token=$ACCESS_TOKEN	Get the feedback received from a buyer or seller in an order
# /feedback/{Feedback_id}&access_token=$ACCESS_TOKEN	Change feedback
# /feedback/{Feedback_Id}/reply	Retrieves data from a feedback given by seller.
# /users/{Seller_id}/order_blacklist	Retrieves all blocked users for bid, on a seller's items






# /users/{User_id}/items_visits?date_from={Date_from}&date_to={Date_to}	Returns how many visits a users had
# /users/{User_id}/items_visits/time_window?last={Last}&unit={Unit}&ending={Ending}	Retrieves visits on every classified item of an user for a certain time window, by site. The information detail it’s grouped by time intervals.
# /users/{User_id}/contacts/questions?date_from={Date_from}&date_to={Date_to}	Retrieve the total questions an specific user had in all of his classified items between a date range.
# /users/{User_id}/contacts/questions/time_window?last={Last}&unit={Unit}	This resource let you get the questions made on a seller classified items for a certain time window.
# /users/{User_id}/contacts/questions/time_window?last={Last}&unit={Unit}	This resource let you get the questions made on a seller classified item for a certain time window.
# /users/{User_id}/contacts/phone_views?date_from={Date_from}&date_to={Date_to}	You can get the total times the ‘See phone’ option was clicked for every item of an user between date ranges.
# /users/{User_id}/contacts/phone_views/time_window?last={Last}&unit={Unit}	You can get the total times the ‘See phone’ option was clicked on an item or for every item of an user on a time window.
# /items/visits?ids={Id1, Id2}&date_from={Date_from}&date_to={Date_to}	Retrieves item's visits (Multi-Get).
# /items/{Item_id}/visits/time_window?last={Last}&unit={Unit}&ending={Ending}	Retrieves item's visits on a time window filtering by unit and ending parameters.
# /items/visits/time_window?ids={Id1, Id2}last={Last}&unit={Unit}&ending={Ending}	Retrieves multiple item's visits on a time window filtering by unit and ending parameters(Multi Get)
# /items/contacts/phone_views/time_window?ids={Id1,Id2}&last={Last}&unit={Unit}&ending={Ending_date}	Retrieves how many time user's clicked on "See phone" for multiple items (Multi Get).




# /shipments/{Shipment_id}	Retrieves all data to make a delivery
# /items/{Item_id}/shipping_options	Retrieves all methods available to send the product. Valid for custom shipments only.
# /sites/{Site_id}/shipping_methods	Retrieves shipping modes available in a country
# /sites/{Site_id}/shipping_services	Retrieves shipping services available in a country
# /sites/{Site_id}/shipping_options?zip_code_from={Zip_code}&zip_code_to={Zip_code}&dimensions={Dimensions}	Retrieves the cost of a shipping. Shipping cost calculator per country
# /users/{Cust_id}/shipping_modes?category_id={Category_id}	Retrieves methods available to list a item of a user
# /users/{Cust_id}/shipping_options?zip_code={Zip_code}&dimensions={Dimensions}	Retrieves the cost of a shipping. Shipping cost calculator
# /users/{Cust_id}/shipping_options?zip_code={Zip_code}&quantity={Quantity}	Retrieves the cost of a shipping. Shipping cost calculator
# /users/{Cust_id}/shipping_preferences	Retrieves all shipping modes and services available to user
# /orders/{Order_id}/shipments	Retrieves data of the shipping methods chosen
# /shipment_labels	Allows print the ticket for send the order
# /shipment_labels?shipment_ids={shipping_id}&response_type=zpl2&access_token={access_token}	Allows print the ticket for send the order in Zebra Format
# /shipment_labels?shipment_ids={shipping_id}&savePdf=Y&access_token={access_token}	Allows print the ticket for send the order in PDF Format


















    def _token(self, response):
        if 'expires_in' in response:
            expires_in = response['expires_in']
            expires_at = time.time() + int(expires_in)
            response['expires_at'] = expires_at
            self.expires_at = expires_at
        return response

    def _get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)

    def _request(self, method, endpoint, params=None, **kwargs):
        _params = {'access_token': self.access_token}
        if params:
            _params.update(params)
        response = requests.request(method, self.BASE_URL + endpoint, params=_params, **kwargs)
        return self._parse(response)

    def _parse(self, response):
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        return r
