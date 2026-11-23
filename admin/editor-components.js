// Blocs utilisables depuis la barre d'outils du champ Contenu de Decap CMS.
(function () {
  'use strict';

  CMS.registerEditorComponent({
    id: 'photo-largeur',
    label: 'Photo réglable',
    fields: [
      {name: 'src', label: 'Photo (nouvelle ou déjà enregistrée)', widget: 'image'},
      {name: 'width', label: 'Largeur maximale à l’écran', widget: 'select', default: '1200', options: [
        {label: '600 px — petite', value: '600'},
        {label: '800 px — moyenne', value: '800'},
        {label: '1200 px — grande', value: '1200'},
        {label: '1600 px — très grande', value: '1600'},
        {label: '100 % — largeur disponible', value: '100%'}
      ]}
    ],
    pattern: /^\[\[photo:(600|800|1200|1600|100%):([^\]\n]+)\]\]$/m,
    fromBlock: function (match) { return {width: match[1], src: match[2]}; },
    toBlock: function (data) { return '[[photo:' + (data.width || '1200') + ':' + data.src + ']]'; },
    toPreview: function (data) {
      const size = data.width === '100%' ? '100%' : (data.width || '1200') + 'px';
      return h('img', {src: data.src, alt: '', style: {width: '100%', maxWidth: size, height: 'auto'}});
    }
  });

  CMS.registerEditorComponent({
    id: 'galerie-position',
    label: 'Galerie à cet endroit',
    fields: [{name: 'number', label: 'Numéro de la galerie (ordre dans « Galeries photos »)', widget: 'number', value_type: 'int', min: 1, default: 1}],
    pattern: /^\[\[galerie:(\d+)\]\]$/m,
    fromBlock: function (match) { return {number: Number(match[1])}; },
    toBlock: function (data) { return '[[galerie:' + (Number(data.number) || 1) + ']]'; },
    toPreview: function (data) { return h('div', {style: {padding: '18px', background: '#e5f2ed', color: '#15583e', borderRadius: '8px'}}, 'Galerie n° ' + data.number + ' — affichée ici sur le site'); }
  });
}());
