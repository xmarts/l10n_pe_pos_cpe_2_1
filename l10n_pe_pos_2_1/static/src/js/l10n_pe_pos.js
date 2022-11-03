odoo.define('l10n_pe_pos_2_1.l10n_pe_pos', function (require) {
"use strict";

var models = require('point_of_sale.models');
const ClientDetailsEdit = require('point_of_sale.ClientDetailsEdit');
var core    = require('web.core');
//var Model = require('web.DataModel');
var rpc = require('web.rpc')
const Registries = require('point_of_sale.Registries');
var PosDB = require('point_of_sale.DB')

var QWeb = core.qweb;

var _t = core._t;

var PosModelSuper = models.PosModel;
var OrderSuper = models.Order;

models.load_fields("res.currency", ["singular_name", "plural_name", "fraction_name", "show_fraction"]);
models.load_fields("res.partner", ["doc_type", "city_id", "doc_number", "nombre_comercial", "estado_contribuyente", "condicion_contribuyente", "state_id", "l10n_pe_district"]);
models.load_fields("res.company", ["street","logo"]);
models.load_fields("pos.order", ["account_move"]);
models.load_fields("pos.config", ["ruc","is_electronic"]);

models.load_models([
    {
        model:  'table.ple.2',
        fields: ['name','code'],
        loaded: function(self, types){
            self.doc_type_by_code = {};
            for (var i = 0; i < types.length; i++) {
                self.doc_type_by_code[types[i].id] = types[i];
            }
            self.doc_types = types;
        },
    },
    {
        model:  'res.city',
        fields: ['name','state_id'],
        loaded: function(self, states_citys){
            self.city_id_by_code = {};
            self.city_id_by_state = {};
            self.state_id_by_country = [];
            for (var i = 0; i < states_citys.length; i++) {
                if (states_citys[i].state_id[0] in self.city_id_by_state === false){
                    self.state_id_by_country.push({'id':states_citys[i].state_id[0], 'name':states_citys[i].state_id[1]})
                    self.city_id_by_state[states_citys[i].state_id[0]] = {}
                }
                self.city_id_by_state[states_citys[i].state_id[0]][states_citys[i].id] = states_citys[i]
                //self.city_id_by_code[states_citys[i].code] = states_citys[i];
            }
            self.city_ids = states_citys;
            self.state_ids = self.state_id_by_country;


        },
    },
    /*{
        model:  'res.country.state',
        fields: ['name'],
        loaded: function(self, country_states){
            self.state_id_by_code = {};
            for (var i = 0; i < country_states.length; i++) {
                self.state_id_by_code[country_states[i].code] = country_states[i];
            }
            self.state_ids = country_states;
        },
    },*/
    {
        model:  'l10n_pe.res.city.district',
        fields: ['name','city_id'],
        loaded: function(self, states_districts){
            self.district_id_by_code = {};
            self.district_id_by_city = {};
            for (var i = 0; i < states_districts.length; i++) {
                if (states_districts[i].city_id[0] in self.district_id_by_city === false){
                    self.district_id_by_city[states_districts[i].city_id[0]] = {}
                }
                self.district_id_by_city[states_districts[i].city_id[0]][states_districts[i].id] = states_districts[i]
                //self.district_id_by_code[states_districts[i].code] = states_districts[i];
            }
            self.district_ids = states_districts;
        },
    }
]);

models.PosModel = models.PosModel.extend({
    initialize: function(session, attributes) {
        var res = PosModelSuper.prototype.initialize.apply(this, arguments);
        return res;
    },
    validate_pe_doc: function (doc_type, doc_number) {
        if (!doc_type || !doc_number){
            return false;
        }
        if (doc_number.length==8 && doc_type=='1') {
            return true;
        }
        else if (doc_number.length==11 && doc_type=='6')
        {
            var vat= doc_number;
            var factor = '5432765432';
            var sum = 0;
            var dig_check = false;
            if (vat.length != 11){
                return false;
            }
            try{
                parseInt(vat)
            }
            catch(err){
                return false; 
            }
            
            for (var i = 0; i < factor.length; i++) {
                sum += parseInt(factor[i]) * parseInt(vat[i]);
             } 

            var subtraction = 11 - (sum % 11);
            if (subtraction == 10){
                dig_check = 0;
            }
            else if (subtraction == 11){
                dig_check = 1;
            }
            else{
                dig_check = subtraction;
            }
            
            if (parseInt(vat[10]) != dig_check){
                return false;
            }
            return true;
        }
        else if (doc_number.length>=3 &&  ['0', '4', '7', 'A'].indexOf(doc_type)!=-1) {
            return true;
        }
        else if (doc_type.length>=2) {
            return true;
        }
        else {
            return false;
        }
    },

});

models.Order = models.Order.extend({
    initialize: function(attributes,options){
        OrderSuper.prototype.initialize.apply(this, arguments);
        this.document_type_id= undefined;
    },
    get_doc_type: function() {
        var client = this.get_client();
        var doc=client ? client.doc_type : "";
        if (doc){
            var doc_type = this.pos.doc_type_by_code[doc[0]].code;    
        }
        else {
            var doc_type = "";   
        }
        return doc_type;
    },
    get_doc_number: function() {
        var client = this.get_client();
        var doc_number=client ? client.doc_number : "";
        return doc_number;
    },
    get_amount_text: function() {
        return numeroALetras(this.get_total_with_tax(), {
          plural: this.pos.currency.plural_name,
          singular: this.pos.currency.singular_name,
          centPlural: this.pos.currency.show_fraction ? this.pos.currency.sfraction_name: "",
          centSingular: this.pos.currency.show_fraction ? this.pos.currency.sfraction_name: ""});
    },

    set_document_type_id: function(document_type_id) {
        this.assert_editable();
        this.document_type_id = document_type_id;
    },
    export_as_JSON: function() {
        var res = OrderSuper.prototype.export_as_JSON.apply(this, arguments);
        res['document_type_id']=this.document_type_id;
        return res;
    },
});

PosDB.include({
    _partner_search_string: function(partner){
        var str =  partner.name || '';
        if(partner.barcode){
            str += '|' + partner.barcode;
        }
        if(partner.address){
            str += '|' + partner.address;
        }
        if(partner.phone){
            str += '|' + partner.phone.split(' ').join('');
        }
        if(partner.mobile){
            str += '|' + partner.mobile.split(' ').join('');
        }
        if(partner.email){
            str += '|' + partner.email;
        }
        if(partner.vat){
            str += '|' + partner.vat;
        }
        if(partner.doc_number){
            str += '|' + partner.doc_number;
        }
        str = '' + partner.id + ':' + str.replace(':','') + '\n';
        return str;
    },
     _product_search_string: function(product){
        var str = product.display_name;
        if (product.barcode) {
            str += '|' + product.barcode;
        }
        if (product.default_code) {
            str += '|' + product.default_code;
        }
        if (product.description) {
            str += '|' + product.description;
        }
        if (product.description_sale) {
            str += '|' + product.description_sale;
        }
        str  = product.id + ':' + str.replace(/:/g,'') + '\n';
        return str;
    },
});

const PePosClientDetailsEdit = ClientDetailsEdit => class extends ClientDetailsEdit {
    constructor() {
        super(...arguments);
        this.intFields = ['city_id', 'l10n_pe_district', 'country_id', 'state_id', 'property_product_pricelist'];
        const partner = this.props.partner;
        this.changes = {
            'city_id': partner.city_id && partner.city_id[0],
            'l10n_pe_district': partner.l10n_pe_district && partner.l10n_pe_district[0],
            'country_id': partner.country_id && partner.country_id[0],
            'state_id': partner.state_id && partner.state_id[0],
        };
    }
    captureChange(event){
        let processedChanges = {};
        this.changes[event.target.name] = event.target.value;
        console.log('123456789')
        if( event.target.name == 'doc_number' || event.target.name == 'doc_type'){
            if (event.target.name == 'doc_type'){
                var doc_type = event.target.value  
            }else{
                if('doc_type' in this.changes){
                    var doc_type = this.changes.doc_type;
                }else{
                    var doc_type = this.props.partner.doc_type;
                }
            }
            if (event.target.name == 'doc_number'){
              var doc_number = event.target.value  
            }else{
                if('doc_number' in this.changes){
                    var doc_number = this.changes.doc_number;
                }else{
                    var doc_number = this.props.partner.doc_number;
                }
            }
            var doc_type_code = '';


            if (doc_type){
                var doc_type_code = this.env.pos.doc_type_by_code[doc_type].code;
                console.log(doc_type_code, doc_number)

                if (doc_number){
                    console.log(doc_type_code, doc_number)
                    this.set_client_details(doc_type_code, doc_number);
                }
            }
        }


    }
    changeState(event){
        var contents = $("select[name='city_id']") ;
        contents.empty()
        var htmlcontent = ''
        htmlcontent += '<option value="">None</option>'

        for(var key in this.env.pos.city_id_by_state[event.target.value]){
            htmlcontent += '<option value="'+this.env.pos.city_id_by_state[event.target.value][key].id+'" >'
            htmlcontent += this.env.pos.city_id_by_state[event.target.value][key].name
            htmlcontent += '</option>'
        }
        contents.append(htmlcontent)
        this.changes[event.target.name] = event.target.value;

    }
    changeCity(event){
        var contents = $("select[name='l10n_pe_district']") ;
        contents.empty()
        var htmlcontent = ''
        htmlcontent += '<option value="">None</option>'

        for(var key in this.env.pos.district_id_by_city[event.target.value]){
            htmlcontent += '<option value="'+this.env.pos.district_id_by_city[event.target.value][key].id+'" >'
            htmlcontent += this.env.pos.district_id_by_city[event.target.value][key].name
            htmlcontent += '</option>'
        }
        contents.append(htmlcontent)
        this.changes[event.target.name] = event.target.value;

    }

    
    saveChanges() {
        let processedChanges = {};
        for (let [key, value] of Object.entries(this.changes)) {
            if (this.intFields.includes(key)) {
                processedChanges[key] = parseInt(value) || false;
            } else {
                processedChanges[key] = value;
            }
        }
        if ((!this.props.partner.name && !processedChanges.name) ||
            processedChanges.name === '' ){
            return this.showPopup('ErrorPopup', {
              title: _('A Customer Name Is Required'),
            });
        }
        var doc_type = processedChanges.doc_type || this.props.partner.doc_type
        var doc_number = processedChanges.doc_number || this.props.partner.doc_number
        if (doc_type && !doc_number && doc_type!="0"){
            return this.showPopup('ErrorPopup', {
              title: _('El número de documento es requerido'),
            });
        }
        if (!doc_type && doc_number){
            return this.showPopup('ErrorPopup', {
              title: _('El Tipo de documento es requerido'),
            });
        }
        processedChanges.id = this.props.partner.id || false;
        this.trigger('save-changes', { processedChanges });
    }

    set_client_details(doc_type, doc_number) {
        var self = this;
        if (doc_type && !doc_number && doc_type!="0"){
            return self.showPopup('ErrorPopup', {
              title: _('El número de documento es requerido'),
            });
        }
        if (!doc_type && doc_number){
            return self.showPopup('ErrorPopup', {
              title: _('El tipo de documento es requerido'),
            });
        }
        if (doc_type && doc_number){
            if (doc_type == "1" || doc_type == "6"){
                if(!self.env.pos.validate_pe_doc(doc_type, doc_number)){
                    return self.showPopup('ErrorPopup', {
                      title: _('El tipo de documento o el número de documento es incorrecto'),
                    });
                }
                else{
                    rpc.query({
                        model:'res.partner',
                        method: 'get_partner_from_ui',
                        args: [doc_type, doc_number]
                    }).then(
                    function(result){
                        if (result.data){
                            if (doc_type == "1"){
                                //contents.find("[name='name']").val(result.data.apellido_paterno+' '+result.data.apellido_materno+', '+result.data.nombres);
                                console.log('CAMBIO 1')
                            }
                            else if (doc_type == "6"){
                                var contents = $('.client-details-contents') ;
                                contents.find("[name='name']").val(result.data.razon_social);
                                contents.find('.nombre_comercial').val(result.data.nombre_comercial);
                                contents.find("[name='street']").val(result.data.domicilio_fiscal);
                                contents.find("[name='estado_contribuyente']").val(result.data.estado_contribuyente);
                                contents.find("[name='condicion_contribuyente']").val(result.data.condicion_contribuyente);
                                if (result.data.state_id){
                                    contents.find("[name='state_id']").val(result.data.state_id);
                                    self.changes['state_id'] = result.data.state_id;
                                }
                                if (result.data.l10n_pe_district){
                                    contents.find("[name='l10n_pe_district']").val(result.data.l10n_pe_district);
                                    self.changes['l10n_pe_district'] = result.data.l10n_pe_district;
                                }
                                if (result.data.city_id){
                                    contents.find("[name='city_id']").val(result.data.city_id);
                                    self.changes['city_id'] = result.data.city_id;
                                }

                                self.changes['name'] = result.data.razon_social;
                                self.changes['nombre_comercial'] = result.data.nombre_comercial;
                                self.changes['street'] = result.data.domicilio_fiscal;
                                self.changes['estado_contribuyente'] = result.data.estado_contribuyente;
                                self.changes['condicion_contribuyente'] = result.data.condicion_contribuyente;
                            }
                        }
                    });
                }
            }
        }
    }   
}


Registries.Component.extend(ClientDetailsEdit, PePosClientDetailsEdit);

return ClientDetailsEdit;
});
