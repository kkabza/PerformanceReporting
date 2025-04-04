USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_TaxCertificateView49]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_TaxCertificateView49](
	[PropertyNumber] [varchar](30) NULL,
	[PropertyUseCode] [varchar](6) NULL,
	[PropertyUseCodeDesc] [varchar](10) NULL,
	[Section] [varchar](6) NULL,
	[Township] [varchar](6) NULL,
	[Range] [varchar](6) NULL,
	[CondoComplex] [varchar](8) NULL,
	[BuildingCount] [int] NULL,
	[LastSaleDate] [date] NULL,
	[QualifiedSale] [char](1) NULL,
	[SalePrice] [decimal](9, 0) NULL,
	[BuildingTypeCode] [varchar](6) NULL,
	[BuildingTypeDesc] [varchar](10) NULL,
	[BldgEffectiveYearBuilt] [int] NULL,
	[BldgHeatedArea] [decimal](9, 0) NULL,
	[BldgActualArea] [decimal](9, 0) NULL,
	[NoOfBedrooms] [int] NULL,
	[NoOfBathrooms] [decimal](3, 1) NULL,
	[ExtraFeatureCode1] [varchar](6) NULL,
	[ExtraFeatureCodeDesc1] [varchar](10) NULL,
	[ExtraFeatureCode2] [varchar](6) NULL,
	[ExtraFeatureCodeDesc2] [varchar](10) NULL,
	[ExtraFeatureCode3] [varchar](6) NULL,
	[ExtraFeatureCodeDesc3] [varchar](10) NULL
) ON [PRIMARY]
GO
